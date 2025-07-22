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

from checkfrench.logger import get_logger


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(pathfile: str, argument: str) -> list[tuple[str, str]]:
    """Parse a CSV file and return each non-empty cell from the specified column with its row number.

    Args:
        pathfile (str): Path to the CSV file (.csv).
        argument (str): Column index (starting from 1) as string.

    Returns:
        list[tuple[str, str]]: List of (row number as string, cell content).
    """
    try:
        col_index: int = int(argument)
        if col_index < 1:
            return []
    except ValueError:
        logger.error("%s is not a valid argument for the csv parser.", argument)
        return []

    results: list[tuple[str, str]] = []

    try:
        with open(pathfile, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader, start=1):
                if len(row) < col_index:
                    continue
                value: str = row[col_index - 1]
                if value.strip():
                    results.append((str(i), value.strip()))
    except Exception as e:
        logger.error("Error when parsing the csv %s : %s", pathfile, e)

    return results
