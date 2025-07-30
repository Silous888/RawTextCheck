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
from gspread import Client, Spreadsheet
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

#     Args:
#         sheet_id (str): id of the sheet

#     Returns:
#         int: 0 if no error, error code otherwise

#     error code:
#     -1 if no credentials file found
#     -2 if credentials not correct
#     -3 if no token, end of waiting time
#     -4 if sheet id not correct
#     """
#     global _current_spreadsheet
#     global _last_sheet
#     global _last_sheet_index

#     ret = __init()
#     if ret != 0:
#         return ret

#     spreadsheet: _gspread.spreadsheet.Spreadsheet = _safe_execute_method(_gc, "open_by_key", sheet_id)
#     # need to check exception

#     _current_spreadsheet = spreadsheet
#     _last_sheet = None
#     _last_sheet_index = None
#     return 0


# def get_sheet_name() -> str | int:
#     if _current_spreadsheet is None:
#         return -4
#     return _safe_execute_method(_current_spreadsheet, "title")


# def _open_sheet(sheet_index: int) -> int:
#     """open a sheet for others functions
#     change the value of the global variables "_last_sheet" and
#     "_last_sheet_index"

#     Args:
#         sheet_index (int): index of the sheet, first is 0

#     Returns:
#         int : 0 if no problem, error code otherwise

#     error code:
#     -3 if no token, end of waiting time
#     -4 if no spreadsheet opened
#     -5 if index not found
#     """
#     global _last_sheet
#     global _last_sheet_index

#     if _current_spreadsheet is None:
#         return -4

#     if sheet_index != _last_sheet_index:
#         last_sheet = _safe_execute_method(_current_spreadsheet, "get_worksheet", sheet_index)
#         # need to check exception
#         _last_sheet = last_sheet
#         _last_sheet_index = sheet_index
#     return 0


# def get_sheet(sheet_index: int) -> (list[list[str]] | int):
#     """get the values in a sheet

#     Args:
#         sheet_index (int): index of the sheet, first is 0

#     Returns:
#         list[list[str]] | int: values in the sheet, error code otherwise

#     error code:
#     -3 if no token, end of waiting time
#     -4 if no spreadsheet opened
#     -5 if index not found
#     """
#     ret = _open_sheet(sheet_index)
#     if ret != 0:
#         return ret
#     return _safe_execute_method(_last_sheet, "get_all_values")
