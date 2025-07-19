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

from checkfrench.default_parameters import JSON_CONFIG_PATH, LANGUAGES, THEMES
from checkfrench.logger import get_logger
from checkfrench.newtype import ItemConfig


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def create_json() -> None:
    if os.path.exists(JSON_CONFIG_PATH):
        return
    data: ItemConfig = ItemConfig(language=LANGUAGES[0][0], theme=THEMES[0][0], hidden_column=[], last_project="")
    with open(JSON_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Created %s.", JSON_CONFIG_PATH)
