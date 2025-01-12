""""main process of the application"""

# -------------------- Import Lib Standard -------------------
import json
from typing import Any

# -------------------- Import Lib User -------------------
from api import google_sheet_api as gsheet
from api import google_drive_api as gdrive
import utils

data_json: dict[str, Any] = {}

ID_SHEET_DICT_GAME: str = "1tjUT3K4kX5_ArT6GXXovWEMf1JmeQRr6_JiqxBCSVrc"


def load_json() -> dict[str, Any]:
    """load json data
    """
    with open("./json_data_jeux.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_list_specific_word(sheet_index: int) -> list[str] | int:
    """get the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        list[str]: list of specific words
    """
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    result: list[list[str]] | int = gsheet.get_sheet(sheet_index)
    if isinstance(result, int):
        return result
    return [item for sublist in result for item in sublist]


def set_list_specific_word(sheet_index: int, list_word: list[str]) -> None:
    """set the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,
        list_word (list[str]): list of specific words
    """
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    rows: int = len(list_word)
    range_to_update: list[str] = [f"A{rows+1}:A"]
    gsheet.clear_sheet_range(sheet_index, range_to_update)
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    gsheet.set_sheet_values(sheet_index, [[word] for word in list_word])


def has_access_to_element(sheet_url: str) -> bool:
    res: bool | int = gdrive.has_access_to_element(utils.extract_google_sheet_id(sheet_url))
    if isinstance(res, bool):
        return res
    return False
