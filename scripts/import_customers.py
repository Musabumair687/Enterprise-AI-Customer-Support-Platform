"""
Import customer records from datasets/customers/customers.csv.

The importer validates required fields, converts dates and monetary values, and
uses each CSV customer_id as an external source ID. Existing source IDs or email
addresses are skipped, so the script can be run again without duplicates.
"""

import csv
import logging
import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from sqlalchemy import or_, select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.models.models import Customer  # noqa: E402


CSV_FILE = PROJECT_ROOT / "datasets" / "customers" / "customers.csv"
REQUIRED_COLUMNS = {"customer_id", "full_name", "email"}


def optional_value(value: str | None) -> str | None:
    """Return stripped text or None when the CSV value is empty."""
    value = (value or "").strip()
    return value or None


def parse_date(value: str | None) -> date | None:
    """Convert an ISO date string from the CSV into a Python date."""
    text = optional_value(value)
    return date.fromisoformat(text) if text else None


def parse_datetime(value: str | None) -> datetime | None:
    """Convert an ISO date-time string from the CSV into a Python datetime."""
    text = optional_value(value)
    return datetime.fromisoformat(text) if text else None


def parse_decimal(value: str | None) -> Decimal | None:
    """Convert a CSV monetary value into Decimal without floating-point loss."""
    text = optional_value(value)
    return Decimal(text) if text else None


def normalize(value: str | None) -> str | None:
    """Normalize status-like values for consistent database storage."""
    text = optional_value(value)
    return text.lower().replace(" ", "_") if text else None


def import_customers() -> None:
    """Validate and import customer rows, logging imported and skipped totals."""
    logger = get_logger()
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Customer CSV file was not found: {CSV_FILE}")

    imported = skipped = invalid = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(f"Customer CSV is missing columns: {sorted(missing_columns)}")

            for row_number, row in enumerate(reader, start=2):
                source_id = optional_value(row.get("customer_id"))
                name = optional_value(row.get("full_name"))
                email = optional_value(row.get("email"))
                if not source_id or not name or not email:
                    invalid += 1
                    logger.warning("Skipped customer row %s: missing required value", row_number)
                    continue

                duplicate = session.scalar(
                    select(Customer.id).where(
                        or_(Customer.external_id == source_id, Customer.email == email)
                    )
                )
                if duplicate is not None:
                    skipped += 1
                    continue

                try:
                    customer = Customer(
                        external_id=source_id,
                        name=name,
                        email=email.lower(),
                        company=optional_value(row.get("company_name")),
                        phone=optional_value(row.get("phone")),
                        country=optional_value(row.get("country")),
                        timezone=optional_value(row.get("timezone")),
                        subscription_plan=optional_value(row.get("subscription_plan")),
                        status=normalize(row.get("account_status")) or "active",
                        registration_date=parse_date(row.get("registration_date")),
                        renewal_date=parse_date(row.get("renewal_date")),
                        last_login=parse_datetime(row.get("last_login")),
                        preferred_language=optional_value(row.get("preferred_language")),
                        support_tier=optional_value(row.get("support_tier")),
                        account_manager=optional_value(row.get("account_manager")),
                        monthly_revenue=parse_decimal(row.get("monthly_revenue")),
                        lifetime_value=parse_decimal(row.get("lifetime_value")),
                    )
                except (ValueError, InvalidOperation) as error:
                    invalid += 1
                    logger.warning("Skipped customer row %s: %s", row_number, error)
                    continue

                session.add(customer)
                imported += 1

        session.commit()
        logger.info(
            "Customer import complete | imported=%s skipped=%s invalid=%s",
            imported,
            skipped,
            invalid,
        )
    except Exception:
        session.rollback()
        logger.exception("Customer import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_customers()
