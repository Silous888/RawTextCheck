"""
File        : json_parser.py
Author      : Silous
Created on  : 2026-03-18
Description : Parser for JSON files.
This module provides a function to parse a JSON file and return non-empty values.
This parser acts as a default parser for JSON files.
"""

# == Imports ==================================================================

import json
from logging import Logger
from typing import Any

from PyQt5.QtCore import QCoreApplication as QCA

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument
from rawtextcheck.ui.messagebox import popup_manager


# == Constants ================================================================

KEY_ARG = ParserArgument(name="key", optional=False)
ID_KEY_ARG = ParserArgument(name="idKey", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [KEY_ARG, ID_KEY_ARG]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def _iter_objects(data: object) -> list[dict[str, Any]]:
    """Recursively collect all dict objects from a JSON structure.

    Args:
        data (object): Parsed JSON data.

    Returns:
        list[dict]: List of all dict objects found.
    """
    objects: list[dict[str, Any]] = []
    if isinstance(data, dict):
        objects.append(data)  # type: ignore
        for value in data.values():  # type: ignore
            objects.extend(_iter_objects(value))  # type: ignore
    elif isinstance(data, list):
        for item in data:  # type: ignore
            objects.extend(_iter_objects(item))  # type: ignore
    return objects


def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a JSON file and return each non-empty value for the specified key.

    Args:
        filepath (str): Path to the JSON file.
        arguments (dict[str, str]): Specific argument for this file.
            keys:
                - "key": The JSON key whose value to extract.
                - "idKey": Optional key to use as row identifier.
                          Defaults to an incrementing index.

    Returns:
        list[tuple[str, str]]: List of (row ID as string, value content).
    """
    try:
        key: str = arguments[KEY_ARG.name]
        id_key: str | None = arguments.get(ID_KEY_ARG.name)
    except KeyError as e:
        logger.error("Missing required argument: %s", e)
        popup_manager.show_error.emit(
            QCA.translate("window title", "Parser Error"),
            QCA.translate("message error", f"Missing required argument {KEY_ARG.name}")
        )
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: object = json.load(f)

        results: list[tuple[str, str]] = []
        index: int = 0

        for obj in _iter_objects(data):
            if key not in obj:
                continue
            value: str = str(obj[key]).strip()
            if not value:
                continue

            if id_key and id_key in obj:
                row_id: str = str(obj[id_key]).strip() or str(index)
            else:
                row_id = str(index)

            results.append((row_id, value))
            index += 1

        return results

    except Exception as e:
        logger.error("Error when parsing the JSON file %s : %s", filepath, e)
        popup_manager.show_error.emit(
            QCA.translate("window title", "Parser Error"),
            QCA.translate("message error", "Error when parsing the JSON file.")
        )
        return []


def replace_text(filepath: str, text: str, line_number: str, arguments: dict[str, str]) -> bool:
    """Replace a given value at position line_number in the JSON file.

    Args:
        filepath (str): Path of the JSON file.
        text (str): New text for the value.
        line_number (str): Row identifier (index or idKey value).
        arguments (dict[str, str]): Specific argument for this file.
            keys:
                - "key": The JSON key whose value to replace.
                - "idKey": Optional key used as row identifier.

    Returns:
        bool: True if the replacement was successful, False otherwise.
    """
    try:
        key: str = arguments[KEY_ARG.name]
        id_key: str | None = arguments.get(ID_KEY_ARG.name)
    except KeyError as e:
        logger.error("Missing required argument: %s", e)
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: object = json.load(f)

        index: int = 0
        target_obj: dict[str, Any] | None = None  # type: ignoa

        for obj in _iter_objects(data):
            if key not in obj:
                continue
            value: str = str(obj[key]).strip()
            if not value:
                continue

            if id_key:
                if id_key in obj and str(obj[id_key]).strip() == line_number:
                    target_obj = obj
                    break
            else:
                if str(index) == line_number:
                    target_obj = obj
                    break

            index += 1

        if target_obj is None:
            logger.error("Row identifier '%s' not found in file %s.", line_number, filepath)
            return False

        target_obj[key] = text

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        logger.error("Error when replacing text in JSON file %s : %s", filepath, e)
        return False