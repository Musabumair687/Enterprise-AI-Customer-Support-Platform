"""
Import employee records from datasets/employees/employees.json.

Creates `Employee` rows. If the dataset does not include an email, a synthetic
email is generated using the `employee_id` to ensure uniqueness.
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
from app.models.models import Employee  # noqa: E402


JSON_FILE = PROJECT_ROOT / "datasets" / "employees" / "employees.json"


def optional_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def make_email(item: dict) -> str:
    emp_id = optional_text(item.get("employee_id"))
    if emp_id:
        return f"{emp_id.lower()}@internal.local"
    name = optional_text(item.get("name")) or "employee"
    safe = "".join(ch for ch in name.lower() if ch.isalnum() or ch == "_")
    return f"{safe}@internal.local"


def import_employees() -> None:
    logger = get_logger()
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"Employees JSON file not found: {JSON_FILE}")

    imported = skipped = invalid = 0
    session_generator = get_db()
    session = next(session_generator)

    try:
        with JSON_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)

        for item in data:
            name = optional_text(item.get("name"))
            if not name:
                invalid += 1
                logger.warning("Skipped employee record with missing name")
                continue

            email = make_email(item)
            exists = session.scalar(select(Employee.id).where(Employee.email == email))
            if exists is not None:
                skipped += 1
                continue

            employee = Employee(
                name=name,
                email=email,
                role=optional_text(item.get("role")) or "support_agent",
                is_active=True,
            )

            session.add(employee)
            imported += 1

        session.commit()
        logger.info("Employee import complete | imported=%s skipped=%s invalid=%s", imported, skipped, invalid)
    except Exception:
        session.rollback()
        logger.exception("Employee import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_employees()
