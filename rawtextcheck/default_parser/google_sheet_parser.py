"""
File        : google_sheet_parser.py
Author      : Silous
Created on  : 2025-07-30
Description : Parser for google sheet.

This module provides a function to parse a google sheet and return non-empty cells of a column.
This parser acts as a default parser for google sheet.
"""


# == Imports ==================================================================

from logging import Logger

from gspread import Spreadsheet, Worksheet
from gspread.exceptions import NoValidUrlKeyFound
from gspread.utils import column_letter_to_index, extract_id_from_url

from rawtextcheck.api import google_sheet_api
from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


# == Constants ================================================================

COL_ARG = ParserArgument(name="col", optional=False)
COL_ID_ARG = ParserArgument(name="colID", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [COL_ARG, COL_ID_ARG]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def is_filepath_valid(filepath: str) -> bool:
    """check if the filepath is a valid file for this parser

    Args:
        filepath (str): path of the file

    Returns:
        bool: True if valid, False otherwise
    """
    if not google_sheet_api.is_credentials_set():
        return False
    try:
        sheet_id: str = extract_id_from_url(filepath)
        spreadsheet: Spreadsheet | None = google_sheet_api.open_spreadsheet(sheet_id)
        if spreadsheet is None:
            return False
        return True
    except NoValidUrlKeyFound:
        return False


def get_filename(filepath: str) -> str:
    """get the filename of the filepath

    Args:
        filepath (str): path of the file

    Returns:
        str: name of the file
    """
    sheet_id: str = extract_id_from_url(filepath)
    spreadsheet: Spreadsheet | None = google_sheet_api.open_spreadsheet(sheet_id)
    if spreadsheet is None:
        return ""
    return google_sheet_api.get_spreadsheet_name(spreadsheet)


def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse a google sheet and return each non-empty cell from the specified column with row identifier.

    Args:
        filepath (str): url of the google sheet.
        argument (str): Column(s), e.g., 'E' or 'E,A'. First is the content column,
                        second (optional) is the row ID column.

    Returns:
        list[tuple[str, str]]: List of (row ID as string, cell content).
    """
    try:
        col_value_index: int = column_letter_to_index(arguments[COL_ARG.name]) - 1  # Always required
        col_id_index: int | None = None
        if COL_ID_ARG.name in arguments.keys():
            col_id_index = column_letter_to_index(arguments[COL_ID_ARG.name]) - 1
    except Exception:
        logger.error("%s is not a valid argument for the google sheet parser.", arguments)
        return []

    id_sheet: str = extract_id_from_url(filepath)

    spreadsheet: Spreadsheet | None = google_sheet_api.open_spreadsheet(id_sheet)
    if spreadsheet is None:
        return []

    worksheet: Worksheet | None = google_sheet_api.open_worksheet(spreadsheet, 0)
    if worksheet is None:
        return []

    values: list[list[str]] | None = google_sheet_api.get_worksheet_values(worksheet)
    if values is None:
        return []

    results: list[tuple[str, str]] = []

    if col_id_index is None:
        for i, line in enumerate(values):
            if not line[col_value_index].strip():
                continue
            results.append((str(i + 1), line[col_value_index]))
    else:
        for i, line in enumerate(values):
            if not line[col_value_index].strip():
                continue
            if line[col_id_index].strip():
                results.append((line[col_id_index], line[col_value_index]))
            else:
                results.append((str(i + 1), line[col_value_index]))

    return results
