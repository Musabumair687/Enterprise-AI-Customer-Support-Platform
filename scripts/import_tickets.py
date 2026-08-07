"""
Import support tickets from datasets/support/tickets.csv.

Each ticket is linked to a Customer using the source customer_id imported by
import_customers.py. Tickets whose customers do not exist are skipped so the
database never contains a broken customer-ticket relationship.
"""

import csv
import logging
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from sqlalchemy import select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.models import Customer, Ticket  # noqa: E402


CSV_FILE = PROJECT_ROOT / "datasets" / "support" / "tickets.csv"
REQUIRED_COLUMNS = {"ticket_id", "customer_id", "created_date", "subject", "message"}
PRIORITY_MAP = {"normal": "medium"}


def optional_value(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


def normalize(value: str | None) -> str | None:
    text = optional_value(value)
    return text.lower().replace(" ", "_") if text else None


def parse_datetime(value: str | None) -> datetime:
    text = optional_value(value)
    if not text:
        raise ValueError("created_date is required")
    return datetime.fromisoformat(text)


def parse_decimal(value: str | None) -> Decimal | None:
    text = optional_value(value)
    return Decimal(text) if text else None


def import_tickets() -> None:
    """Validate and import tickets while preserving customer relationships."""
    logger = get_logger()
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Ticket CSV file was not found: {CSV_FILE}")

    imported = skipped = invalid = missing_customer = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(f"Ticket CSV is missing columns: {sorted(missing_columns)}")

            for row_number, row in enumerate(reader, start=2):
                source_id = optional_value(row.get("ticket_id"))
                customer_source_id = optional_value(row.get("customer_id"))
                title = optional_value(row.get("subject"))
                description = optional_value(row.get("message"))
                if not source_id or not customer_source_id or not title or not description:
                    invalid += 1
                    logger.warning("Skipped ticket row %s: missing required value", row_number)
                    continue

                if session.scalar(select(Ticket.id).where(Ticket.external_id == source_id)) is not None:
                    skipped += 1
                    continue

                customer_id = session.scalar(
                    select(Customer.id).where(Customer.external_id == customer_source_id)
                )
                if customer_id is None:
                    missing_customer += 1
                    logger.warning(
                        "Skipped ticket row %s: customer %s does not exist",
                        row_number,
                        customer_source_id,
                    )
                    continue

                try:
                    priority = normalize(row.get("priority")) or "medium"
                    ticket = Ticket(
                        external_id=source_id,
                        title=title,
                        description=description,
                        status=normalize(row.get("status")) or "open",
                        priority=PRIORITY_MAP.get(priority, priority),
                        department=optional_value(row.get("department")),
                        category=optional_value(row.get("category")),
                        assigned_agent_name=optional_value(row.get("assigned_agent")),
                        resolution=optional_value(row.get("resolution")),
                        sentiment=normalize(row.get("sentiment")),
                        resolution_time_hours=parse_decimal(row.get("resolution_time")),
                        is_escalated=normalize(row.get("escalation")) == "yes",
                        customer_id=customer_id,
                        created_at=parse_datetime(row.get("created_date")),
                    )
                except (ValueError, InvalidOperation) as error:
                    invalid += 1
                    logger.warning("Skipped ticket row %s: %s", row_number, error)
                    continue

                session.add(ticket)
                imported += 1

        session.commit()
        logger.info(
            "Ticket import complete | imported=%s skipped=%s invalid=%s missing_customers=%s",
            imported,
            skipped,
            invalid,
            missing_customer,
        )
    except Exception:
        session.rollback()
        logger.exception("Ticket import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_tickets()
