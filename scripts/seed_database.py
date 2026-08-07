"""
Master database seeder.

Runs the import pipeline in the required order so the database can be seeded
with customers, employees, products, billing, tickets, known issues, feature
requests, and conversation history.
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"
if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

from app.config import get_settings  # noqa: E402
from app.core.logging import configure_logging, get_logger  # noqa: E402

from scripts.import_customers import import_customers  # noqa: E402
from scripts.import_employees import import_employees  # noqa: E402
from scripts.import_products import import_products  # noqa: E402
from scripts.import_billing import import_billing  # noqa: E402
from scripts.import_tickets import import_tickets  # noqa: E402
from scripts.import_known_issues import import_known_issues  # noqa: E402
from scripts.import_feature_requests import import_feature_requests  # noqa: E402
from scripts.import_conversations import import_conversations  # noqa: E402


def seed_database() -> None:
    logger = get_logger()
    logger.info("Starting database seed run")

    steps = [
        ("customers", import_customers),
        ("employees", import_employees),
        ("products", import_products),
        ("billing", import_billing),
        ("tickets", import_tickets),
        ("known issues", import_known_issues),
        ("feature requests", import_feature_requests),
        ("conversations", import_conversations),
    ]

    for name, step in steps:
        logger.info("Seeding %s...", name)
        try:
            step()
        except Exception:
            logger.exception("Database seed failed at step: %s", name)
            raise

    logger.info("Database seed complete")


if __name__ == "__main__":
    configure_logging(get_settings())
    seed_database()
