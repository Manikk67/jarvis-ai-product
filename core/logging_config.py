"""Centralized logging configuration for JARVIS AI."""

import logging
from pathlib import Path

from core.paths import PROJECT_ROOT


def setup_logging(level: int = logging.INFO) -> None:
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "jarvis.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
