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
from PyQt5.QtCore import QCoreApplication as QCA

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument
from rawtextcheck.ui.messagebox import popup_manager


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
        popup_manager.show_error.emit(QCA.translate("window title", "Parser Error"),
                                      QCA.translate("message error",
                                                    "Error when parsing the PO file.")
                                      )
        return []

def replace_text(filepath: str, text: str, line_number: str, arguments: dict[str, str]) -> bool:
    """Replace a given msgstr at position line_number in the PO file.

    Args:
        filepath (str): Path of the PO file.
        text (str): New text for the msgstr.
        line_number (str): Row identifier (line number or msgid value).
        arguments (dict[str, str]): Specific argument for this file.
            keys:
                - "id": Optional identifier, can be "line" or "msgid".
    Returns:
        bool: True if the replacement was successful, False otherwise.
    """
    try:
        po: polib.POFile = polib.pofile(filepath)
        use_msgid: bool = arguments.get(ID_ARG.name, "line") == "msgid"

        target_entry = None
        for entry in po:
            if use_msgid:
                if entry.msgid == line_number:
                    target_entry = entry
                    break
            else:
                row_id: str = str(entry.linenum + 1) if entry.linenum else "?"
                if row_id == line_number:
                    target_entry = entry
                    break

        if target_entry is None:
            logger.error("Row identifier '%s' not found in file %s.", line_number, filepath)
            return False

        target_entry.msgstr = text
        po.save(filepath)
        return True

    except Exception as e:
        logger.error("Error when replacing text in PO file %s : %s", filepath, e)
        return False