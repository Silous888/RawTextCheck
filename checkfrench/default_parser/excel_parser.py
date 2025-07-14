"""
File        : textfile_parser.py
Author      : Silous
Created on  : 2025-06-15
Description : Parser for plain text files.

This module provides a function to parse a text file and return its non-empty lines.
This parser acts as a default parser for text files.
"""


# == Imports ==================================================================

from openpyxl import Workbook, load_workbook
from openpyxl.utils import column_index_from_string


# == Functions ================================================================

def parse_file(pathfile: str, argument: str) -> list[tuple[str, str]]:
    """Parse an Excel file and return each non-empty cell from the specified column with its row number.

    Args:
        pathfile (str): Path to the Excel file (.xlsx).
        argument (str): Column header name to extract values from.

    Returns:
        list[tuple[str, str]]: List of (row number as string, cell content).
    """
    """Parse an Excel file and return non-empty cells from the specified column (given by letter) with their row number.

    Args:
        pathfile (str): Path to the Excel file (.xlsx).
        argument (str): Column letter (e.g., 'A', 'B', 'C') to extract values from.

    Returns:
        list[tuple[str, str]]: List of (row number as string, cell content).
    """
    try:
        col_index: int = column_index_from_string(argument.upper())
    except ValueError:
        return []

    try:
        wb: Workbook = load_workbook(pathfile, data_only=True)
        ws = wb.active

        results: list[tuple[str, str]] = []
        if ws is not None:
            for row in ws.iter_rows(min_row=1):  # Include all rows
                if col_index > len(row):
                    continue  # Skip if the column is out of bounds

                cell = row[col_index - 1]
                if cell.value is not None and str(cell.value).strip():
                    results.append((str(cell.row), str(cell.value)))

        return results

    except Exception:
        return []
