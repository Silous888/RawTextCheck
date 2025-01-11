import gspread as _gspread
from oauth2client.service_account import ServiceAccountCredentials as _sac

import os as _os
import time as _time

try:
    from credentials import credentials_info as _credentials_info
    _MODULE_EXIST = True
except ImportError:
    _MODULE_EXIST = False

_scope = ["https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive"]

_is_credentials_file_exists = True
_is_credentials_correct = True

_credentials_email = None

_credentials_path = ".\\credentials.json"
_gc = None
_current_spreadsheet = None
_last_sheet = None
_last_sheet_index = None

_MAX_RETRIES = 500
_WAIT_TIME = 10


def __init() -> int:
    """init access to google drive

    Returns:
        int: 0 if access are given, otherwise, return an error code.

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    """
    global _is_credentials_correct
    global _is_credentials_file_exists
    global _gc
    global _credentials_email
    if _gc is None:
        if _MODULE_EXIST:
            try:
                credentials = _sac.from_json_keyfile_dict(_credentials_info, _scope)
                _credentials_email = credentials.service_account_email
                _gc = _gspread.authorize(credentials)
                _is_credentials_correct = True
            except Exception:
                _is_credentials_correct = False
        elif _os.path.exists("credentials.json"):
            try:
                credentials = _sac.from_json_keyfile_name(_credentials_path, _scope)
                _credentials_email = credentials.service_account_email
                _gc = _gspread.authorize(credentials)
                _is_credentials_correct = True
            except Exception:
                _is_credentials_correct = False
        else:
            _is_credentials_file_exists = False
    if not _is_credentials_file_exists:
        return -1
    if not _is_credentials_correct:
        return -2
    return 0


def set_credentials_path(credentials_path=".\\credentials.json") -> None:
    """change the path of the credentials, if json file,
    if you give a folder, the path will be credentials_path + "credentials.json
    the path will be set, even if the path doesn't exist yet.

    Args:
        credentials_path (str, optional): path of the folder or file. Defaults to ".\\credentials.json".
    """
    global _credentials_path
    if _os.path.isdir(credentials_path):
        _credentials_path = _os.path.join(credentials_path, "credentials.json")
    if _os.path.isfile(credentials_path):
        _credentials_path = credentials_path


def _decorator_wait_token(func):
    """wait for token if necessary

    Args:
        func (func): function to decorate, first return need to be a boolean of success of the function

    Returns:
        Tuple: returns of the decorated functions, except the first result. If no token after waiting, -1
    """
    def wrapper(*args, **kwargs):
        for _ in range(_MAX_RETRIES):
            results = func(*args, **kwargs)
            if isinstance(results, tuple) and results[0]:
                if len(results[1:]) > 1:
                    return results[1:]
                else:
                    return results[1]
            elif results:
                return results
            _time.sleep(_WAIT_TIME)
        return -3
    return wrapper


@_decorator_wait_token
def open_spreadsheet(sheet_id: str) -> int:
    """open a sheet for others functions

    Args:
        sheet_id (str): id of the sheet

    Returns:
        int: 0 if no error, error code otherwise

    error code:
    -1 if no credentials file found
    -2 if credentials not correct
    -3 if no token, end of waiting time
    -4 if sheet id not correct
    """
    global _current_spreadsheet
    global _last_sheet
    global _last_sheet_index

    ret = __init()
    if ret != 0:
        return ret

    try:
        spreadsheet = _gc.open_by_key(sheet_id)
    except Exception as e:
        if "Response [404]" in str(e):
            return True, -4
        return False
    else:
        _current_spreadsheet = spreadsheet
        _last_sheet = None
        _last_sheet_index = None
        return True, 0


@_decorator_wait_token
def _open_sheet(sheet_index: int) -> int:
    """open a sheet for others functions
    change the value of the global variables "_last_sheet" and
    "_last_sheet_index"

    Args:
        sheet_index (int): index of the sheet, first is 0

    Returns:
        int : 0 if no problem, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    global _last_sheet
    global _last_sheet_index

    if _current_spreadsheet is None:
        return True, -4

    if sheet_index != _last_sheet_index:
        try:
            last_sheet = _current_spreadsheet.get_worksheet(sheet_index)
        except Exception as e:
            if "not found" in str(e):
                return True, -5
            return False
        else:
            _last_sheet = last_sheet
            _last_sheet_index = sheet_index
            return True, 0


@_decorator_wait_token
def get_sheet(sheet_index: int) -> (list[list[str]] | int):
    """get the values in a sheet

    Args:
        sheet_index (int): index of the sheet, first is 0

    Returns:
        list[list[str]] | int: values in the sheet, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    ret = _open_sheet(sheet_index)
    if ret != 0:
        return ret
    try:
        values = _last_sheet.get_all_values()
    except Exception:
        return False
    else:
        return True, values


@_decorator_wait_token
def get_cell_range(sheet_index: int, range: str) -> (list[list[str]] | int):
    """get the values in the selected range in a sheet

    Args:
        sheet_index (int): index of the sheet, first is 0
        range (str): range of the values wanted (ex: 'A1:C3')

    Returns:
        list[list[str]] | int: values in the sheet, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    ret = _open_sheet(sheet_index)
    if ret != 0:
        return ret
    try:
        values = _last_sheet.range(range)
    except Exception:
        return False
    else:
        return True, values


@_decorator_wait_token
def get_cell(sheet_index: int, row: int, col: int) -> (str | int):
    """get the values in the selected range in a sheet

    Args:
        sheet_index (int): index of the sheet, first is 0
        range (str): range of the values wanted (ex: 'A1:C3')

    Returns:
        str | int: values in the sheet, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    ret = _open_sheet(sheet_index)
    if ret != 0:
        return ret
    try:
        value = _last_sheet.cell(row, col)
    except Exception:
        return False
    else:
        return True, value
