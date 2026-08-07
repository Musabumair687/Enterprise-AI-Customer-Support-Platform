"""
Import product records from datasets/products/products.json.

Creates `Product` rows using the product `name` as the unique key.
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
from app.models.models import Product  # noqa: E402


JSON_FILE = PROJECT_ROOT / "datasets" / "products" / "products.json"


def optional_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def import_products() -> None:
    logger = get_logger()
    if not JSON_FILE.exists():
        raise FileNotFoundError(f"Products JSON file not found: {JSON_FILE}")

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
                logger.warning("Skipped product record with missing name")
                continue

            exists = session.scalar(select(Product.id).where(Product.name == name))
            if exists is not None:
                skipped += 1
                continue

            product = Product(
                name=name,
                description=optional_text(item.get("description")),
                version=optional_text(item.get("version")),
                is_active=(str(item.get("status", "")).lower() == "active"),
            )

            session.add(product)
            imported += 1

        session.commit()
        logger.info("Product import complete | imported=%s skipped=%s invalid=%s", imported, skipped, invalid)
    except Exception:
        session.rollback()
        logger.exception("Product import failed; transaction rolled back.")
        raise
    finally:
        session_generator.close()


if __name__ == "__main__":
    configure_logging(get_settings())
    import_products()
