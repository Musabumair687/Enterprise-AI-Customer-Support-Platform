"""
Import billing records from datasets/billing/billing.csv.

Billing rows are linked to customers through source customer_id values. Invoice
numbers are unique, making the import safe to rerun without duplicate invoices.
The resulting records support future billing, refund, and finance features.
"""

import csv
import logging
import sys
from datetime import date
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
from app.models.models import Billing, Customer  # noqa: E402


CSV_FILE = PROJECT_ROOT / "datasets" / "billing" / "billing.csv"
REQUIRED_COLUMNS = {"invoice_id", "customer_id", "amount", "currency", "payment_status"}


def optional_value(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


def normalize(value: str | None) -> str | None:
    text = optional_value(value)
    return text.lower().replace(" ", "_") if text else None


def parse_date(value: str | None) -> date | None:
    text = optional_value(value)
    return date.fromisoformat(text) if text else None


def import_billing() -> None:
    """Validate and import invoices and payments linked to existing customers."""
    logger = get_logger()
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Billing CSV file was not found: {CSV_FILE}")

    imported = skipped = invalid = missing_customer = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(f"Billing CSV is missing columns: {sorted(missing_columns)}")

            for row_number, row in enumerate(reader, start=2):
                invoice_number = optional_value(row.get("invoice_id"))
                customer_source_id = optional_value(row.get("customer_id"))
                currency = optional_value(row.get("currency"))
                if not invoice_number or not customer_source_id or not currency:
                    invalid += 1
                    logger.warning("Skipped billing row %s: missing required value", row_number)
                    continue
                if len(currency) != 3:
                    invalid += 1
                    logger.warning("Skipped billing row %s: currency must use 3 letters", row_number)
                    continue
                if session.scalar(select(Billing.id).where(Billing.invoice_number == invoice_number)) is not None:
                    skipped += 1
                    continue

                customer_id = session.scalar(
                    select(Customer.id).where(Customer.external_id == customer_source_id)
                )
                if customer_id is None:
                    missing_customer += 1
                    logger.warning(
                        "Skipped billing row %s: customer %s does not exist",
                        row_number,
                        customer_source_id,
                    )
                    continue

                try:
                    billing = Billing(
                        customer_id=customer_id,
                        invoice_number=invoice_number,
                        plan=optional_value(row.get("plan")),
                        amount=Decimal((row.get("amount") or "").strip()),
                        currency=currency.upper(),
                        status=normalize(row.get("payment_status")) or "pending",
                        record_type="invoice",
                        payment_method=optional_value(row.get("payment_method")),
                        due_date=parse_date(row.get("due_date")),
                        paid_date=parse_date(row.get("paid_date")),
                        refund_status=normalize(row.get("refund_status")),
                    )
                except (ValueError, InvalidOperation) as error:
                    invalid += 1
                    logger.warning("Skipped billing row %s: %s", row_number, error)
                    continue

                session.add(billing)
                imported += 1

        session.commit()
        logger.info(
            "Billing import complete | imported=%s skipped=%s invalid=%s missing_customers=%s",
            imported,
            skipped,
            invalid,
            missing_customer,
        )
    except Exception:
        session.rollback()
        logger.exception("Billing import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_billing()
