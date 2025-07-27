"""
File        : logger.py
Author      : Silous
Created on  : 2025-04-26
Description : Module for configuring logging in the application.

This module sets up a logging configuration that includes both file and console handlers.

Features:
- File logging with rotation
- Console logging
- Custom log format
"""


# == Imports ==================================================================

import logging
import os
from logging.handlers import RotatingFileHandler


# == Constants ================================================================

LOG_FOLDER = "logs"
LOG_LEVEL = logging.DEBUG  # Global log level
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB per file
BACKUP_COUNT = 3  # Keep 3 old log files (log.1, log.2, etc.)
LOGFILE_NAME = "rawtextcheck"


os.makedirs(LOG_FOLDER, exist_ok=True)


# == Functions ================================================================

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for the specified module name.
    Args:
        name (str): The name of the logger, typically the module name.
    Returns:
        logging.Logger: A configured logger instance.
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False  # hide log file_handler in console

    if not logger.handlers:  # Avoid adding multiple handlers if already created
        # File handler per module
        file_handler = RotatingFileHandler(
            filename=os.path.join(LOG_FOLDER, f"{LOGFILE_NAME}.log"),
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(filename)s:%(lineno)d: %(message)s"
        ))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "[%(levelname)s] %(filename)s:%(lineno)d: %(message)s"
        ))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
