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

LIST_ARGUMENTS: list[ParserArgument] = []


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a file and return each non-empty line with its line number.

    Args:
        filepath (str): Path of the file.
        argument (str): Specific argument for this file (not used).

    Returns:
        list[tuple[str, str]]: List of tuples (line number as string, line content).
    """
    lines: list[tuple[str, str]] = []
    try:

        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                stripped: str = line.strip()
                if stripped:
                    lines.append((str(i), stripped))

        return lines
    except UnicodeDecodeError as e:
        logger.error("Error when parsing the textfile %s : %s", filepath, e)
        return lines
