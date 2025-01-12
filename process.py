""""main process of the application"""

# -------------------- Import Lib Standard -------------------
import json
from typing import Any

# -------------------- Import Lib User -------------------
from api import google_sheet_api as gsa

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
    gsa.open_spreadsheet(ID_SHEET_DICT_GAME)
    result: list[list[str]] | int = gsa.get_sheet(sheet_index)
    if isinstance(result, int):
        return result
    return [item for sublist in result for item in sublist]


def set_list_specific_word(sheet_index: int, list_word: list[str]) -> None:
    """set the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,
        list_word (list[str]): list of specific words
    """
    gsa.open_spreadsheet(ID_SHEET_DICT_GAME)
    rows: int = len(list_word)
    range_to_update: list[str] = [f"A{rows+1}:A"]
    gsa.clear_sheet_range(sheet_index, range_to_update)
    gsa.open_spreadsheet(ID_SHEET_DICT_GAME)
    print(gsa.set_sheet_values(sheet_index, [[word] for word in list_word]))
