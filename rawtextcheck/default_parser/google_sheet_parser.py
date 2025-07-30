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
from gspread.utils import column_letter_to_index, extract_id_from_url

from rawtextcheck.api import google_sheet_api
from rawtextcheck.script import json_config
from rawtextcheck.logger import get_logger


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def parse_file(pathfile: str, argument: str) -> list[tuple[str, str]]:
    """Parse a google sheet and return each non-empty cell from the specified column with row identifier.

    Args:
        pathfile (str): url of the google sheet.
        argument (str): Column(s), e.g., 'E' or 'E,A'. First is the content column,
                        second (optional) is the row ID column.

    Returns:
        list[tuple[str, str]]: List of (row ID as string, cell content).
    """
    try:
        parts: list[str] = [arg.strip().upper() for arg in argument.split(",")]
        col_value_index: int = column_letter_to_index(parts[0]) - 1 # Always required
        col_id_index: int | None = column_letter_to_index(parts[1]) - 1 if len(parts) > 1 else None
    except Exception:
        logger.error("%s is not a valid argument for the google sheet parser.", argument)
        return []

    google_sheet_api.set_credentials_info(json_config.load_data()['credentials_google'])
    id_sheet: str = extract_id_from_url(pathfile)

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
            results.append((str(i), line[col_value_index]))
    else:
        for i, line in enumerate(values):
            if not line[col_value_index].strip():
                continue
            if line[col_id_index].strip():
                results.append((line[col_id_index], line[col_value_index]))
            else:
                results.append((str(i), line[col_value_index]))

    return results