"""
Import historical conversation records from datasets/conversation_history/conversation_history.json.

Stores each chat message as a Conversation row, grouped by conversation session.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from sqlalchemy import select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.models import Conversation, Customer, Ticket  # noqa: E402

JSON_FILE = PROJECT_ROOT / "datasets" / "conversation_history" / "conversation_history.json"


def optional_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_timestamp(value: str | None) -> datetime | None:
    text = optional_text(value)
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def normalize_role(value: str | None) -> str:
    text = optional_text(value)
    if not text:
        return "unknown"
    return text.lower().replace(" ", "_")


def import_conversations() -> None:
    logger = get_logger()
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"Conversation JSON file not found: {JSON_FILE}")

    imported = skipped = invalid = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with JSON_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        for item in data:
            session_id = optional_text(item.get("conversation_id"))
            customer_source_id = optional_text(item.get("customer_id"))
            timestamp = parse_timestamp(item.get("timestamp"))
            if not session_id or not customer_source_id or not timestamp:
                invalid += 1
                logger.warning("Skipped conversation entry with missing required metadata")
                continue

            if session.scalar(select(Conversation.id).where(Conversation.session_id == session_id)) is not None:
                skipped += 1
                continue

            customer_id = session.scalar(
                select(Customer.id).where(Customer.external_id == customer_source_id)
            )
            if customer_id is None:
                skipped += 1
                logger.warning(
                    "Skipped conversation %s: customer %s does not exist",
                    session_id,
                    customer_source_id,
                )
                continue

            ticket_id = None
            linked_ticket = optional_text(item.get("linked_ticket"))
            if linked_ticket:
                ticket_id = session.scalar(select(Ticket.id).where(Ticket.external_id == linked_ticket))

            messages = item.get("messages") or []
            if not isinstance(messages, list) or not messages:
                invalid += 1
                logger.warning("Skipped conversation %s: no messages", session_id)
                continue

            for message in messages:
                content = optional_text(message.get("content"))
                if not content:
                    continue
                conversation = Conversation(
                    customer_id=customer_id,
                    ticket_id=ticket_id,
                    session_id=session_id,
                    sender_role=normalize_role(message.get("role")),
                    content=content,
                    created_at=timestamp,
                )
                session.add(conversation)

            imported += 1

        session.commit()
        logger.info(
            "Conversation import complete | imported=%s skipped=%s invalid=%s",
            imported,
            skipped,
            invalid,
        )
    except Exception:
        session.rollback()
        logger.exception("Conversation import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_conversations()
