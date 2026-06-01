"""
Utility for setting up logging with optional local file logging.

This module provides a function to configure logging for applications.
It sets up a logger with a specified logging level and can output logs
to both the console and a file, based on user preference.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def setup_logging(local_log: bool = False) -> logging.Logger:
    log_level = logging.INFO
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if local_log:
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
