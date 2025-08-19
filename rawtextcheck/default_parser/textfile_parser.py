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

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


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
        argument (dict[str, str]): Specific argument for this file (not used).

    Returns:
        list[tuple[str, str]]: List of tuples (line number as string, line content).
    """
    begin_line_number = None
    if BEGIN_LINE_NUMBER.name in arguments.keys():
        try:
            begin_line_number = int(arguments[BEGIN_LINE_NUMBER.name])
        except:
            logger.error("%s not a valid argument for %s.",
                         arguments[BEGIN_LINE_NUMBER.name],
                         BEGIN_LINE_NUMBER.name)

    end_line_number = None
    if END_LINE_NUMBER.name in arguments.keys():
        try:
            end_line_number = int(arguments[END_LINE_NUMBER.name])
        except Exception as e:
            logger.error("%s not a valid argument for %s.",
                         arguments[END_LINE_NUMBER.name],
                         END_LINE_NUMBER.name)

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

                if CONTAINS.name in arguments.keys() and arguments[CONTAINS.name] not in line:
                  continue
                if NOT_CONTAINS.name in arguments.keys() and arguments[NOT_CONTAINS.name] in line:
                  continue

                stripped: str = line.strip()
                if stripped:
                    lines.append((str(i), stripped))

        return lines
    except UnicodeDecodeError as e:
        logger.error("Error when parsing the textfile %s : %s", filepath, e)
        return lines
