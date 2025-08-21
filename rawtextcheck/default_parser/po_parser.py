"""
File        : po_parser.py
Author      : Silous
Created on  : 2025-08-19
Description : Parser for PO files.

This module provides a function to parse a .po file and return non-empty translations.
This parser acts as a default parser for PO files.
"""

# == Imports ==================================================================

from logging import Logger
import polib

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


# == Constants ================================================================

ID_ARG = ParserArgument(name="id", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [ID_ARG]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a PO file and return each non-empty translation.

    Args:
        filepath (str): Path to the .po file.
        arguments (dict[str, str]): Specific argument for this file.
        keys:
            - "id": Optional identifier for the row, can be "line" or "msgid".

    Returns:
        list[tuple[str, str]]: List of (row identifier, msgstr).
    """
    try:
        po: polib.POFile = polib.pofile(filepath)

        results: list[tuple[str, str]] = []

        use_msgid: bool = arguments.get(ID_ARG.name, "line") == "msgid"

        for entry in po:
            if entry.msgstr and entry.msgstr.strip():
                if use_msgid:
                    row_id = entry.msgid
                else:
                    # polib garde la position dans entry.linenum
                    row_id: str = str(entry.linenum + 1) if entry.linenum else "?"
                results.append((row_id, entry.msgstr))

        return results

    except Exception as e:
        logger.error("Error when parsing the PO file %s : %s", filepath, e)
        return []
