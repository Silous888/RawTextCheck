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
    """Parse a CSV file and return each non-empty cell from the specified column with its row identifier.

    Args:
        pathfile (str): Path to the CSV file (.csv).
        argument (str): Column index (starting from 1), or "4,1" where:
                        - first is content column
                        - second (optional) is row ID column

    Returns:
        list[tuple[str, str]]: List of (row ID as string, cell content).
    """
    try:
        parts = [int(a.strip()) for a in argument.split(",")]
        col_value_index = parts[0]
        col_id_index = parts[1] if len(parts) > 1 else None

        if col_value_index < 1 or (col_id_index is not None and col_id_index < 1):
            return []
    except ValueError:
        logger.error("%s is not a valid argument for the CSV parser.", argument)
        return []

    results: list[tuple[str, str]] = []

    try:
        with open(pathfile, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader, start=1):
                if len(row) < col_value_index:
                    continue

                value: str = row[col_value_index - 1].strip()
                if value:
                    if col_id_index is not None and len(row) >= col_id_index:
                        row_id = row[col_id_index - 1].strip()
                        if not row_id:
                            row_id = str(i)
                    else:
                        row_id = str(i)

                    results.append((row_id, value))
    except Exception as e:
        logger.error("Error when parsing the CSV %s : %s", pathfile, e)

    return results
