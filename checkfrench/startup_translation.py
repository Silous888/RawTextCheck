"""
File        : startup_translation.py
Author      : Silous
Created on  : 2025-07-26
Description : Handles application translations.

This module initializes the translation system for the CheckFrench application.
It loads the appropriate translation file based on the user's language setting.

Warning:
Some code is a copy of the code in json_config.py and default_parameters.py
to avoid issue with elements not translated because the modules are imported
before the translation is initialized.
"""


# == Imports ==================================================================

import json
from logging import Logger
import os
import sys

from PyQt5.QtCore import QTranslator

from checkfrench.logger import get_logger
from checkfrench.newtype import ItemConfig


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)

CONFIG_FOLDER = 'config'
"""Folder where config files are stored,
same as in default_parameters.py"""

JSON_CONFIG_PATH = CONFIG_FOLDER + '/config.json'
"""Path to the JSON file containing app configuration,
same as in default_parameters.py"""

DEFAULT_LANGUAGE = 'english'
"""Default language for the application,
same as in default_parameters.py"""

DEFAULT_THEME = 'light'
"""Default theme for the application,
same as in default_parameters.py"""


# == Functions ================================================================

def load_data_config() -> ItemConfig:
    """return current settings of the app

    Returns:
        ItemConfig: every attribute of the configuration in an object
    """
    if not os.path.exists(JSON_CONFIG_PATH):
        logger.warning("Configuration file does not exist yet: %s", JSON_CONFIG_PATH)
        return ItemConfig(language=DEFAULT_LANGUAGE, theme=DEFAULT_THEME,
                          hidden_column=[], last_project="", credentials_google={})
    with open(JSON_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    logger.info("Loaded app configuration data")


def translations_path(relative_path: str) -> str:
    """Get the absolute path to a translation file.
    This function handles both development and PyInstaller environments.
    Args:
        relative_path (str): The relative path to the translation file.
    Returns:
        str: The absolute path to the translation file.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: resource is in the _internal folder
        base_path: str = sys._MEIPASS  # type: ignore
        return os.path.join(base_path, 'translations', relative_path)  # type: ignore
    else:
        # Dev: resource is in local 'translations' directory
        return os.path.join('translations', relative_path)


def init_translator() -> QTranslator | None:
    """Initialize the translator for the application.
    Returns:
        QTranslator | None: The translator object if successful, None otherwise.
    """
    translator = QTranslator()

    if translator.load(translations_path(load_data_config()["language"] + ".qm")):
        return translator
    return None
