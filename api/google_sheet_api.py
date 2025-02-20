import gspread as _gspread
from oauth2client.service_account import ServiceAccountCredentials as _sac
import os as _os
import time as _time
from typing import Callable, Any

try:
    from credentials import credentials_info as _credentials_info
    _MODULE_EXIST = True
except ImportError:
    _MODULE_EXIST = False

_scope: list[str] = ["https://spreadsheets.google.com/feeds",
                     "https://www.googleapis.com/auth/spreadsheets",
                     "https://www.googleapis.com/auth/drive.file",
                     "https://www.googleapis.com/auth/drive"]

_is_credentials_file_exists = True
_is_credentials_correct = True

_credentials_email = None

_credentials_path = ".\\credentials.json"
_gc = None
_current_spreadsheet = None
_last_sheet : _gspread.Worksheet | None = None
_last_sheet_index: int | None = None

_MAX_RETRIES = 100
_WAIT_TIME = 5


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


def set_credentials_path(credentials_path: str = ".\\credentials.json") -> None:
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


def _safe_execute_method(obj: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
    """Execute a method of an object with given arguments in a try-except block,
       until it works or the maximum number of retries is reached.

    Args:
        obj (Any): The object containing the method.
        method_name (str): The name of the method to execute.
        *args (Any): Positional arguments for the method.
        **kwargs (Any): Keyword arguments for the method.

    Returns:
        Any: The result of the method if it succeeds, otherwise None.
    """
    method = getattr(obj, method_name)
    for _ in range(_MAX_RETRIES):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            if "429" not in str(e):
                print(e)
                return -11  # to define later
        _time.sleep(_WAIT_TIME)
    return -10  # max retries reached


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

    spreadsheet: _gspread.spreadsheet.Spreadsheet = _safe_execute_method(_gc, "open_by_key", sheet_id)
    # need to check exception

    _current_spreadsheet = spreadsheet
    _last_sheet = None
    _last_sheet_index = None
    return 0


def get_sheet_name() -> str | int:
    if _current_spreadsheet is None:
        return -4
    return _safe_execute_method(_current_spreadsheet, "title")


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
        return -4

    if sheet_index != _last_sheet_index:
        last_sheet = _safe_execute_method(_current_spreadsheet, "get_worksheet", sheet_index)
        # need to check exception
        _last_sheet = last_sheet
        _last_sheet_index = sheet_index
        return 0


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
    return _safe_execute_method(_last_sheet, "get_all_values")


def get_values_range(sheet_index: int, range: str) -> (list[list[str]] | int):
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
    return _safe_execute_method(_last_sheet, "get_values", range)


def get_value_column(sheet_index: int, column: int) -> (list[str] | int):
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
    return _safe_execute_method(_last_sheet, "col_values", column)


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
    return _safe_execute_method(_last_sheet, "cell", row, col)


def set_sheet_values(sheet_index: int, values: list[list[str]]) -> int:
    """Set the values in a sheet

    Args:
        sheet_index (int): index of the sheet, first is 0
        values (list[list[str]]): values to set in the sheet

    Returns:
        int: 0 if no error, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    ret = _open_sheet(sheet_index)
    if ret != 0:
        return ret

    rows = len(values)
    cols = len(values[0]) if rows > 0 else 0
    range_to_update = f"A1:{chr(65 + cols - 1)}{rows}" if rows > 0 and cols > 0 else None

    if range_to_update is None:
        print("Erreur : Plage invalide ou vide.")
        return -7  # Code d'erreur pour plage vide

    # Mise à jour des valeurs dans la feuille
    result = _safe_execute_method(_last_sheet, "update", range_to_update, values)

    if result is None or result == -10 or result == -11:
        return -1  # Erreur générique ou quota atteint
    return 0


def clear_sheet_range(sheet_index: int, ranges: list[str]) -> int:
    """Set the values in a sheet

    Args:
        sheet_index (int): index of the sheet, first is 0
        values (list[list[str]]): values to set in the sheet

    Returns:
        int: 0 if no error, error code otherwise

    error code:
    -3 if no token, end of waiting time
    -4 if no spreadsheet opened
    -5 if index not found
    """
    ret = _open_sheet(sheet_index)
    if ret != 0:
        return ret
    ret = _safe_execute_method(_last_sheet, "batch_clear", ranges)

    return ret
