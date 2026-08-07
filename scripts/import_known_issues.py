"""
Import known issues from datasets/support/known_issues.json.

Creates `KnownIssue` rows and links them to `Product` when a matching product
name exists.
"""

import json
import logging
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from sqlalchemy import select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.models import KnownIssue, Product  # noqa: E402


JSON_FILE = PROJECT_ROOT / "datasets" / "support" / "known_issues.json"


def optional_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def import_known_issues() -> None:
    logger = get_logger()
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"Known issues JSON not found: {JSON_FILE}")

    imported = skipped = invalid = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with JSON_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        for item in data:
            title = optional_text(item.get("title"))
            description = optional_text(item.get("description"))
            if not title or not description:
                invalid += 1
                logger.warning("Skipped known issue with missing title/description")
                continue

            product_name = optional_text(item.get("product_name"))
            product_id = None
            if product_name:
                product_id = session.scalar(select(Product.id).where(Product.name == product_name))

            ki = KnownIssue(
                title=title,
                description=description,
                severity=optional_text(item.get("severity")) or "medium",
                status=optional_text(item.get("status")) or "open",
                workaround=optional_text(item.get("workaround")),
                product_id=product_id,
            )

            session.add(ki)
            imported += 1

        session.commit()
        logger.info("Known issues import complete | imported=%s skipped=%s invalid=%s", imported, skipped, invalid)
    except Exception:
        session.rollback()
        logger.exception("Known issues import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_known_issues()
