"""
File        : excel_parser.py
Author      : Silous
Created on  : 2025-07-19
Description : Parser for excel files.

This module provides a function to parse a excel file and return non-empty cells of a column.
This parser acts as a default parser for excel files.
"""


# == Imports ==================================================================

from logging import Logger

from openpyxl import Workbook, load_workbook, cell
from openpyxl.utils import column_index_from_string
from PyQt5.QtCore import QCoreApplication as QCA

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument
from rawtextcheck.ui.messagebox import popup_manager


# == Constants ================================================================

COL_ARG = ParserArgument(name="col", optional=False)
COL_ID_ARG = ParserArgument(name="colID", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [COL_ARG, COL_ID_ARG]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse an Excel file and return each non-empty cell from the specified column with row identifier.

    Args:
        filepath (str): Path to the Excel file (.xlsx).
        argument (dict[str, str]): Specific argument for this file.
            keys:
                - "col": Column letter (e.g., "A") to parse.
                - "colID": Optional column letter for row identifier (default is the row number).

    Returns:
        list[tuple[str, str]]: List of (row ID as string, cell content).
    """
    try:
        col_value_index: int = column_index_from_string(arguments[COL_ARG.name])
        col_id_index: int | None = None
        if COL_ID_ARG.name in arguments.keys():
            col_id_index = column_index_from_string(arguments[COL_ID_ARG.name])
    except ValueError:
        logger.error("%s is not a valid argument for the excel parser.", arguments)
        popup_manager.show_error.emit(QCA.translate("window title", "Parser Error"),
                                      QCA.translate("message error",
                                                    f"{arguments} is not a valid argument for the excel parser.")
                                      )
        return []

    try:
        wb: Workbook = load_workbook(filepath, data_only=True)
        ws = wb.active

        results: list[tuple[str, str]] = []

        if ws is not None:
            for row in ws.iter_rows(min_row=1):
                if col_value_index > len(row):
                    continue  # Value column out of range

                cell_value = row[col_value_index - 1]

                if cell_value.value is not None and str(cell_value.value).strip():
                    if col_id_index is not None and col_id_index <= len(row):
                        cell_id = row[col_id_index - 1]
                        row_id: str = str(cell_id.value).strip() if cell_id.value is not None else str(cell_value.row)
                    else:
                        row_id = str(cell_value.row)

                    results.append((row_id, str(cell_value.value)))

        return results

    except Exception as e:
        logger.error("Error when parsing the Excel file %s : %s", filepath, e)
        popup_manager.show_error.emit(QCA.translate("window title", "Parser Error"),
                                      QCA.translate("message error",
                                                    "Error when parsing the Excel file.")
                                      )
        return []

def replace_text(filepath: str, text: str, line_number: str, arguments: dict[str, str]) -> bool:
    """Replace a given text at position line_number in the specified column.

    Args:
        filepath (str): Path of the Excel file.
        text (str): New text for the cell.
        line_number (str): Row identifier (row number or colID value).
        arguments (dict[str, str]): Specific argument for this file.
            keys:
                - "col": Column letter (e.g., "A") to replace.
                - "colID": Optional column letter for row identifier.
    Returns:
        bool: True if the replacement was successful, False otherwise.
    """
    try:
        col_value_index: int = column_index_from_string(arguments[COL_ARG.name])
        col_id_index: int | None = None
        if COL_ID_ARG.name in arguments:
            col_id_index = column_index_from_string(arguments[COL_ID_ARG.name])
    except ValueError:
        logger.error("Invalid arguments for Excel replace_text: %s", arguments)
        return False

    try:
        wb: Workbook = load_workbook(filepath)
        ws = wb.active
        if ws is None:
            logger.error("No active sheet found in file %s.", filepath)
            return False

        target_row = None
        for row in ws.iter_rows(min_row=1):
            if col_id_index is not None:
                if col_id_index <= len(row):
                    cell_id = row[col_id_index - 1]
                    if cell_id.value is not None and str(cell_id.value).strip() == line_number:
                        target_row = row
                        break
            else:
                if col_value_index <= len(row):
                    cell_value = row[col_value_index - 1]
                    if str(cell_value.row) == line_number:
                        target_row = row
                        break

        if target_row is None:
            logger.error("Row identifier '%s' not found in file %s.", line_number, filepath)
            return False

        if col_value_index > len(target_row):
            logger.error("Column index %s out of range in file %s.", col_value_index, filepath)
            return False

        target_cell = target_row[col_value_index - 1]
        if not isinstance(target_cell, cell.cell.Cell):
            logger.error("Cell at column %s is a merged cell in file %s.", col_value_index, filepath)
            return False

        target_cell.value = text
        wb.save(filepath)
        return True

    except OSError as e:
        logger.error("Error when replacing text in Excel file %s : %s", filepath, e)
        return False