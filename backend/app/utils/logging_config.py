import logging
import os
import sys


def setup_logging():
    """
    Centralized logging configuration.
    Logs to stdout (Docker-friendly).
    Log level configurable via environment variable.
    """

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Reduce noise from uvicorn access logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)