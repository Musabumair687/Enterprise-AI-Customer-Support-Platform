"""Logging configuration and request logging middleware."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import perf_counter

from fastapi import Request
from starlette.responses import Response

from app.config import Settings


LOGGER_NAME = "enterprise_support"
LOG_DIRECTORY = Path(__file__).resolve().parents[2] / "logs"
LOG_FILE = LOG_DIRECTORY / "application.log"


def get_logger() -> logging.Logger:
    """Return the application's shared logger."""
    return logging.getLogger(LOGGER_NAME)


def configure_logging(settings: Settings) -> logging.Logger:
    """Configure terminal and rotating file logs from application settings."""
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logger = get_logger()
    logger.setLevel(settings.log_level)
    logger.propagate = False

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


async def request_logging_middleware(request: Request, call_next) -> Response:
    """Log every request, including its response status and duration."""
    logger = get_logger()
    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed | method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            elapsed_ms,
        )
        raise

    elapsed_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "Request completed | method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response
