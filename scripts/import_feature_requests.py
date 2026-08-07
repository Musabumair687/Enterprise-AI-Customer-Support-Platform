"""
Import feature requests from datasets/support/feature_requests.csv.

Finds customers by `external_id` and products by name when available.
"""

import csv
import logging
import sys
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from sqlalchemy import select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.models import FeatureRequest, Customer, Product  # noqa: E402


CSV_FILE = PROJECT_ROOT / "datasets" / "support" / "feature_requests.csv"


def optional_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_date(value: str | None):
    text = optional_text(value)
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except Exception:
        return None


def import_feature_requests() -> None:
    logger = get_logger()
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Feature requests CSV not found: {CSV_FILE}")

    imported = skipped = invalid = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            for row_number, row in enumerate(reader, start=2):
                title = optional_text(row.get("title"))
                description = optional_text(row.get("description"))
                customer_ext = optional_text(row.get("customer_id"))
                product_name = optional_text(row.get("product_name"))

                if not title or not description or not customer_ext:
                    invalid += 1
                    logger.warning("Skipped feature request row %s: missing required value", row_number)
                    continue

                customer_id = session.scalar(select(Customer.id).where(Customer.external_id == customer_ext))
                if customer_id is None:
                    skipped += 1
                    logger.warning("Skipped feature request row %s: customer not found (%s)", row_number, customer_ext)
                    continue

                product_id = None
                if product_name:
                    product_id = session.scalar(select(Product.id).where(Product.name == product_name))

                fr = FeatureRequest(
                    title=title,
                    description=description,
                    status=optional_text(row.get("status")) or "submitted",
                    priority=optional_text(row.get("priority")) or "medium",
                    customer_id=customer_id,
                    product_id=product_id,
                )

                session.add(fr)
                imported += 1

        session.commit()
        logger.info("Feature request import complete | imported=%s skipped=%s invalid=%s", imported, skipped, invalid)
    except Exception:
        session.rollback()
        logger.exception("Feature request import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_feature_requests()
