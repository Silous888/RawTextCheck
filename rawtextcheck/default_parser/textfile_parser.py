"""
File        : textfile_parser.py
Author      : Silous
Created on  : 2025-07-19
Description : Parser for plain text files.

This module provides a function to parse a text file and return its non-empty lines.
This parser acts as a default parser for text files.
"""

# == Imports ==================================================================

from logging import Logger

from PyQt5.QtCore import QCoreApplication as QCA

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument
from rawtextcheck.ui.messagebox import popup_manager


# == Constants ================================================================

BEGIN_TEXT = ParserArgument(name="beginText", optional=True)
END_TEXT = ParserArgument(name="endText", optional=True)
BEGIN_LINE_NUMBER = ParserArgument(name="beginLineNumber", optional=True)
END_LINE_NUMBER = ParserArgument(name="endLineNumber", optional=True)
CONTAINS = ParserArgument(name="contains", optional=True)
NOT_CONTAINS = ParserArgument(name="notContains", optional=True)


LIST_ARGUMENTS: list[ParserArgument] = [BEGIN_TEXT, END_TEXT,
                                        BEGIN_LINE_NUMBER, END_LINE_NUMBER,
                                        CONTAINS, NOT_CONTAINS]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a file and return each non-empty line with its line number.

    Args:
        filepath (str): Path of the file.
        arguments (dict[str, str]): Specific argument for this file.
        keys:
            - "beginText": Optional text to start parsing from.
                        Not used if "beginLineNumber" is provided.
            - "endText": Optional text to stop parsing at.
                        Not used if "endLineNumber" is provided.
            - "beginLineNumber": Optional line number to start parsing from.
            - "endLineNumber": Optional line number to stop parsing at.
            - "contains": Optional substring that each line must contain.
            - "notContains": Optional substring that each line must not contain.

    Returns:
        list[tuple[str, str]]: List of tuples (line number as string, line content).
    """
    begin_line_number = None
    if BEGIN_LINE_NUMBER.name in arguments.keys():
        try:
            begin_line_number = int(arguments[BEGIN_LINE_NUMBER.name])
        except Exception:
            logger.error("%s not a valid argument for %s.",
                         arguments[BEGIN_LINE_NUMBER.name],
                         BEGIN_LINE_NUMBER.name)
            popup_manager.show_error.emit(
                QCA.translate("window title", "Parser Error"),
                QCA.translate(
                    "message error",
                    f"{arguments[BEGIN_LINE_NUMBER.name]} is not a valid argument for {BEGIN_LINE_NUMBER.name}.")
                )

    end_line_number = None
    if END_LINE_NUMBER.name in arguments.keys():
        try:
            end_line_number = int(arguments[END_LINE_NUMBER.name])
        except Exception:
            logger.error("%s not a valid argument for %s.",
                         arguments[END_LINE_NUMBER.name],
                         END_LINE_NUMBER.name)
            popup_manager.show_error.emit(
                QCA.translate("window title", "Parser Error"),
                QCA.translate(
                    "message error",
                    f"{arguments[END_LINE_NUMBER.name]} is not a valid argument for {END_LINE_NUMBER.name}.")
                )

    contains_vals: list[str] = []
    if CONTAINS.name in arguments:
        contains_vals = [val.strip() for val in arguments[CONTAINS.name].split("|") if val.strip()]

    not_contains_vals: list[str] = []
    if NOT_CONTAINS.name in arguments:
        not_contains_vals = [val.strip() for val in arguments[NOT_CONTAINS.name].split("|") if val.strip()]

    is_begin_text_found = False
    lines: list[tuple[str, str]] = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):

                if begin_line_number:
                    if i < begin_line_number:
                        continue
                elif BEGIN_TEXT.name in arguments.keys():
                    if arguments[BEGIN_TEXT.name] == line.strip():
                        is_begin_text_found = True
                    elif not is_begin_text_found:
                        continue

                if end_line_number:
                    if i >= end_line_number:
                        break
                elif END_TEXT.name in arguments.keys():
                    if arguments[END_TEXT.name] == line.strip():
                        break

                if contains_vals and not all(val in line for val in contains_vals):
                    continue

                if not_contains_vals and any(val in line for val in not_contains_vals):
                    continue

                stripped: str = line.strip()
                if stripped:
                    lines.append((str(i), stripped))

        return lines
    except UnicodeDecodeError as e:
        logger.error("Error when parsing the textfile %s : %s", filepath, e)
        popup_manager.show_error.emit(QCA.translate("window title", "Parser Error"),
                                      QCA.translate("message error",
                                                    "Error when parsing the text file. "
                                                    "The file might not be a valid UTF-8 text file.")
                                      )
        return lines

def replace_text(filepath: str, text: str, line_number: str) -> bool:
    """Replace a given text at position line_number

    Args:
        filepath (str): Path of the file.
        text (str): Text for a unique line
        line_number (str): Number or id of the line
    """
    try:
        target: int = int(line_number)
    except ValueError:
        logger.error("Invalid line number: %s", line_number)
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines: list[str] = f.readlines()

        if target < 1 or target > len(lines):
            logger.error("Line number %s out of range (file has %s lines).", line_number, len(lines))
            return False

        original_line: str = lines[target - 1]
        ending: str = "\n" if original_line.endswith("\n") else ""
        lines[target - 1] = text + ending

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return True

    except OSError as e:
        logger.error("Error when replacing text in file %s : %s", filepath, e)
        return False