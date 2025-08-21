"""
File        : csv_parser.py
Author      : Silous
Created on  : 2025-07-19
Description : Parser for CSV files.

This module provides a function to parse a CSV file and return its non-empty lines
from the specified column. The first column starts at 1.
"""

# == Imports ==================================================================

import csv
from logging import Logger

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


# == Constants ================================================================

COL_ARG = ParserArgument(name="col", optional=False)
COL_ID_ARG = ParserArgument(name="colID", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [COL_ARG, COL_ID_ARG]

# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a CSV file and return each non-empty cell from the specified column with its row identifier.

    Args:
        filepath (str): Path to the CSV file (.csv).
        argument (str): Specific argument for this file.
            keys:
                - "col": Column number (1-based index) to parse.
                - "colID": Optional column number (1-based index) for row
                        identifier (default is the row number).

    Returns:
        list[tuple[str, str]]: List of (row ID as string, cell content).
    """
    try:
        col_value_index: int = int(arguments[COL_ARG.name])
        col_id_index: int | None = None
        if COL_ID_ARG.name in arguments.keys():
            col_id_index = int(arguments[COL_ID_ARG.name])
        if col_value_index < 1 or (col_id_index is not None and col_id_index < 1):
            return []

    except ValueError:
        logger.error("%s is not a valid argument for the CSV parser.", arguments)
        return []

    results: list[tuple[str, str]] = []

    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader, start=1):
                if len(row) < col_value_index:
                    continue

                value: str = row[col_value_index - 1].strip()
                if value:
                    if col_id_index is not None and len(row) >= col_id_index:
                        row_id: str = row[col_id_index - 1].strip()
                        if not row_id:
                            row_id = str(i)
                    else:
                        row_id = str(i)

                    results.append((row_id, value))
    except Exception as e:
        logger.error("Error when parsing the CSV %s : %s", filepath, e)

    return results
