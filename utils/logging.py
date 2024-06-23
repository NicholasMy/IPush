import logging
import os
import time
from logging.handlers import RotatingFileHandler


def configure_logging():
    logging.Formatter.converter = time.gmtime  # Use UTC
    os.makedirs("logs", exist_ok=True)
    log_file: str = "logs/ipush.log"
    log_format: str = "%(asctime)s [%(levelname)s] %(message)s"
    app_logger = logging.getLogger("ipush")
    app_logger.setLevel("DEBUG")
    handler = RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=100, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(log_format))
    app_logger.addHandler(handler)

    logger = get_app_logger(__name__)
    logger.info(f"Starting IPush")
    logger.info("(Log timestamps are in UTC)")


def get_app_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(f"ipush.{module_name}")
