""""main process of the application"""

# -------------------- Import Lib Standard -------------------
import json
from typing import Any

# -------------------- Import Lib User -------------------
from api import google_sheet_api as gsheet
from api import google_drive_api as gdrive
import orthocheck
import utils

data_json: dict[str, Any] = {}

ID_SHEET_DICT_GAME: str = "1tjUT3K4kX5_ArT6GXXovWEMf1JmeQRr6_JiqxBCSVrc"

id_current_game: int = 0
list_excluded_word_current_game: list[str] = []


def load_json() -> dict[str, Any]:
    """load json data
    """
    with open("./json_data_games.json", "r", encoding="utf-8") as file:
        return json.load(file)


def set_id_and_word_list(id: int, list_word: list[str]) -> None:
    global id_current_game
    global list_excluded_word_current_game
    id_current_game = id
    list_excluded_word_current_game = list_word


def get_list_specific_word(sheet_index: int) -> int:
    """get the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    if sheet_index + 1 == id_current_game:
        return 0
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    result: list[list[str]] | int = gsheet.get_sheet(sheet_index)
    if isinstance(result, int):
        return result
    set_id_and_word_list(sheet_index + 1, [item for sublist in result for item in sublist])
    return 0


def set_list_specific_word(list_word: list[str]) -> None:
    """set the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,
        list_word (list[str]): list of specific words
    """
    list_word.sort()
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    range_to_update: list[str] = ["A:A"]
    gsheet.clear_sheet_range(id_current_game - 1, range_to_update)
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    gsheet.set_sheet_values(id_current_game - 1, [[word] for word in list_word])
    set_id_and_word_list(id_current_game, list_word)


def has_access_to_element(sheet_url: str) -> bool:
    res: bool | int = gdrive.has_access_to_element(utils.extract_google_sheet_id(sheet_url))
    if isinstance(res, bool):
        return res
    return False


def orthocheck_load_dictionary() -> None:
    """call load_words of orthocheck
    """
    orthocheck.load_words("dictionary_orthocheck")
