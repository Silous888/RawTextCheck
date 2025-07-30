"""
File        : google_sheet_api.py
Author      : Silous
Created on  : 2025-07-28
Description : Simple API to access Google Sheets using gspread.

"""


# == Imports ==================================================================

from logging import Logger
import time
from typing import Any

import gspread
from gspread import Client, Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials  # type: ignore

from rawtextcheck.logger import get_logger


# == Constants ===============================================================

MAX_RETRIES = 30
WAIT_TIME = 5


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)

SCOPE: list[str] = ["https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive.file",
                    "https://www.googleapis.com/auth/drive"]

gc: Client | None = None


# == Functions ================================================================

def set_credentials_info(credentials_info: dict[str, Any]) -> None:
    """Set the credentials information for Google Sheets API.
    Args:
        credentials_info (dict[str, Any]): The credentials information as a dictionary.
    """
    global gc
    if gc is None:
        try:
            credentials: ServiceAccountCredentials = (
                ServiceAccountCredentials.from_json_keyfile_dict(  # type: ignore
                    credentials_info, SCOPE  # type: ignore
                )
            )
            gc = gspread.authorize(credentials)  # type: ignore
            logger.info("Google Sheets credentials set successfully.")
        except ValueError as e:
            logger.error("Credentials not correctly set in config: %s", e)
    else:
        logger.warning("Credentials already set, skipping.")


def _safe_execute_method(obj: Any, method_name: str, *args: Any, **kwargs: Any) -> Any | Exception:
    """Execute a method of an object with given arguments in a try-except block,
       until it works or the maximum number of retries is reached.

    Args:
        obj (Any): The object containing the method.
        method_name (str): The name of the method to execute.
        *args (Any): Positional arguments for the method.
        **kwargs (Any): Keyword arguments for the method.

    Returns:
        Any: The result of the method if it succeeds, otherwise an Exception.
    """
    method = getattr(obj, method_name)

    logger.info("Trying method: %s on %s", method_name, obj)
    logger.info("Arguments: %s, Keyword Arguments: %s", args, kwargs)

    for attempt in range(MAX_RETRIES):
        try:
            logger.info("Attempt %s of %s", attempt + 1, MAX_RETRIES)
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            if "429" in str(e) or "500" in str(e) or "503" in str(e):
                logger.info("Waiting for token, retry in %s seconds, error: %s", WAIT_TIME, e)
                time.sleep(WAIT_TIME)
                continue

            # method_name will manage log of the error
            return e

    logger.error("After %s retries, failed to execute %s.", MAX_RETRIES, method_name)
    return RuntimeError("MAX_RETRIES")



def open_spreadsheet(sheet_id: str) -> Spreadsheet | None:
    """open a sheet for others functions

    Args:
        sheet_id (str): id of the sheet

    Returns:
        Spreadsheet | None: Spreadsheet object, or None if error.
    """
    global _current_spreadsheet
    global _last_sheet
    global _last_sheet_index

    if gc is None:
        logger.error("Credentials not set.")
        return

    spreadsheet: Spreadsheet | Exception = _safe_execute_method(gc, "open_by_key", sheet_id)
    if isinstance(spreadsheet, Exception):
        if "MAX_RETRIES" not in str(spreadsheet):
            logger.error("Spreadsheet %s can't be opened, error: %s", sheet_id, spreadsheet)
        return
    return spreadsheet


def get_spreadsheet_name(spreadsheet: Spreadsheet) -> str | None:
    """Get the name of a spreadsheet

    Args:
        spreadsheet (Spreadsheet): an opened spreadsheet

    Returns:
        str: name of the spreadsheet
    """
    return spreadsheet.title
    

def open_worksheet(spreadsheet: Spreadsheet, sheet_index: int) -> Worksheet | None:
    """open a Worksheet for others functions

    Args:
        spreadsheet (Spreadsheet): spreadsheet of the worksheet
        sheet_index (int): index of the worksheet, first is 0

    Returns:
        Worksheet | None: Worksheet object, or None if error.
    """
    worksheet: Worksheet | Exception = _safe_execute_method(spreadsheet, "get_worksheet", sheet_index)
    if isinstance(worksheet, Exception):
        if "MAX_RETRIES" not in str(worksheet):
            logger.error("Worksheet %s of spreadsheet name:%s, id:%s can't be opened, error: %s",
                         sheet_index, spreadsheet.title, spreadsheet.id, worksheet)
        return
    return worksheet


def get_worksheet_values(worksheet: Worksheet) -> (list[list[str]] | None):
    """get the values in a worksheet
    length is (last row with value, last col with value)
    every list[str] will have the same lenght.
    empty cell will be an empty string

    Args:
        worksheet (Worksheet): worksheet opened

    Returns:
        list[list[str]] | None: values in the worksheet, or None if error
    """
    values: list[list[str]] | Exception = _safe_execute_method(worksheet, "get_all_values")
    if isinstance(values, Exception):
        if "MAX_RETRIES" not in str(worksheet):
            logger.error("Can't get values of worksheet name:%s, id:%s", worksheet.title, worksheet.id)
        return
    return values