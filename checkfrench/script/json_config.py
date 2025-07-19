"""
File        : json_config.py
Author      : Silous
Created on  : 2025-07-19
Description : Manage config file of the software.


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
    doesn't exist
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
    with open(JSON_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data() -> ItemConfig:
    with open(JSON_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)[0]


def set_language(language: str) -> None:
    data: ItemConfig = load_data()
    data["language"] = language
    save_data(data)


def set_theme(theme: str) -> None:
    data: ItemConfig = load_data()
    data["theme"] = theme
    save_data(data)


def set_hidden_column(hidden_column: list[str]) -> None:
    data: ItemConfig = load_data()
    data["hidden_column"] = hidden_column
    save_data(data)


def set_last_project(last_project: str) -> None:
    data: ItemConfig = load_data()
    data["last_project"] = last_project
    save_data(data)
