"""
File        : json_config.py
Author      : Silous
Created on  : 2025-07-19
Description : Manage config file of the software.

The config file is a json with one ItemConfig.
It defines app language and theme, and has 2 parameters to remember
last state of the UI: the project selected and the column hidden in
the tableresult.
"""

# == Imports ==================================================================

import json
from logging import Logger
import os

from checkfrench.default_parameters import CONFIG_FOLDER, JSON_CONFIG_PATH, LANGUAGES, THEMES
from checkfrench.logger import get_logger
from checkfrench.newtype import ItemConfig


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def create_json() -> None:
    """create json for app config if the file
    doesn't exist with a default ItemConfig
    """
    if os.path.exists(JSON_CONFIG_PATH):
        return

    os.makedirs(CONFIG_FOLDER, exist_ok=True)

    data: ItemConfig = ItemConfig(language=LANGUAGES[0][0],
                                  theme=THEMES[0][0],
                                  hidden_column=[],
                                  last_project="")
    save_data(data)
    logger.info("Created %s.", JSON_CONFIG_PATH)


def save_data(data: ItemConfig) -> None:
    """update data in the json of the config
    will overwrite everything

    Args:
        data (ItemConfig): new values for the config
    """
    with open(JSON_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data() -> ItemConfig:
    """return current settings of the app

    Returns:
        ItemConfig: every attribute of the configuration in an object
    """
    with open(JSON_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    logger.info("Loaded app configuration data")


def set_language(language: str) -> None:
    """Update the language of the app

    Args:
        language (str): new language
    """
    data: ItemConfig = load_data()
    data["language"] = language
    save_data(data)
    logger.info("App configuration language set to %s", data["language"])


def set_theme(theme: str) -> None:
    """Update the theme of the app

    Args:
        theme (str): name of the new theme
    """
    data: ItemConfig = load_data()
    data["theme"] = theme
    save_data(data)
    logger.info("App configuration theme set to %s", data["theme"])


def set_hidden_column(hidden_column: list[str]) -> None:
    """Update default hidden column of tableresult

    Args:
        hidden_column (list[str]): name of every column hidden by default
    """
    data: ItemConfig = load_data()
    data["hidden_column"] = hidden_column
    save_data(data)
    logger.info("App configuration hidden column set to %s", data["hidden_column"])


def set_last_project(last_project: str) -> None:
    """Update last project opened

    Args:
        last_project (str): name of the last project opened
    """
    data: ItemConfig = load_data()
    data["last_project"] = last_project
    save_data(data)
    logger.info("App configuration last project set to %s", data["last_project"])
