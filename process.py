""""main process of the application"""

# -------------------- Import Lib Standard -------------------
import json
import os
import re
from typing import Any

# -------------------- Import Lib User -------------------
from api import google_sheet_api as gsheet
from api import google_drive_api as gdrive
import orthocheck
import utils

data_json: dict[str, Any] = {}

ID_SHEET_DICT_GAME: str = "1tjUT3K4kX5_ArT6GXXovWEMf1JmeQRr6_JiqxBCSVrc"

LIST_METHOD_FOLDER_NAME: list[str] = ["methode 1 - dictionnaire",
                                      "methode 2 - MS Word",
                                      "methode 3 - LanguageTool"]

id_current_game: int = 0
list_specific_word_current_game: list[str] = []
list_sentences_current_sheet: list[str] = []

list_specific_word_to_upload: list[str] = []


def load_json() -> dict[str, Any]:
    """load json data
    """
    with open("./json_data_games.json", "r", encoding="utf-8") as file:
        return json.load(file)


def set_id_and_word_list(id: int, list_word: list[str]) -> None:
    global id_current_game
    global list_specific_word_current_game
    id_current_game = id
    list_specific_word_current_game = list_word


def get_list_specific_word(sheet_index: int) -> int:
    """get the list of specific words of a game in the sheet

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    output: list[list[str]] | int = gsheet.get_sheet(sheet_index)
    if isinstance(output, int):
        return output
    set_id_and_word_list(sheet_index + 1, [item for sublist in output for item in sublist])
    return 0


def get_list_sentence_sheet(url_sheet: str, column_letter: str,
                            insert_space_substrings: bool, insert_space_codes: bool) -> int:
    """get the list of specific words of a game in the sheet

    Args:
        url_sheet (int): url of the sheet
        column_letter (str): column of the sheet to get
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        int : 0 if no problem, error code otherwise
    """
    global list_sentences_current_sheet
    gsheet.open_spreadsheet(utils.extract_google_sheet_id(url_sheet))
    num_column: int = utils.get_position_letter_alphabet(column_letter)
    sheet_extraction: list[str] | int = gsheet.get_value_column(0, num_column)
    if isinstance(sheet_extraction, int):
        return sheet_extraction
    ignored_substrings: dict[str, str] = data_json[id_current_game - 1]["ignored_substrings"]  # type: ignore
    ignored_codes: list[str] = data_json[id_current_game - 1]["ignored_codes"]  # type: ignore
    list_sentences_current_sheet = [
        remove_ignored_codes(
            remove_ignored_substrings(sentence, ignored_substrings, insert_space_substrings),
            ignored_codes,
            insert_space_codes
        ) for sentence in sheet_extraction
    ]
    return 0


def set_list_specific_word(list_word: list[str]) -> None:
    """set the list of specific words of a game in the sheet

    Args:
        list_word (list[str]): list of specific words
    """
    list_word.sort()
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    range_to_update: list[str] = ["A:A"]
    gsheet.clear_sheet_range(id_current_game - 1, range_to_update)
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    gsheet.set_sheet_values(id_current_game - 1, [[word] for word in list_word])
    set_id_and_word_list(id_current_game, list_word)


def add_list_specific_word() -> None:
    """add the list of specific words in the sheet
    """
    global list_specific_word_current_game, list_specific_word_to_upload
    get_list_specific_word(id_current_game - 1)
    list_specific_word_current_game = list_specific_word_current_game + list_specific_word_to_upload
    list_specific_word_current_game.sort()
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    gsheet.set_sheet_values(id_current_game - 1, [[word] for word in list_specific_word_current_game])
    list_specific_word_to_upload.clear()


def get_name_sheet(sheet_url: str) -> str | int:
    """call has_access_to_element of google_drive_api
    """
    try:
        output: str | int = gdrive.get_name_by_id(utils.extract_google_sheet_id(sheet_url))
        if isinstance(output, str):
            return output
    except Exception:
        return -1
    return -2


def remove_ignored_substrings(text: str, ignored_substrings: dict[str, str], insert_space: bool) -> str:
    """Remove substrings from text that are enclosed by any of the ignored substrings.

    Args:
        text (str): The input text.
        ignored_substrings (dict[str, str]): A dictionary where keys are the starting
        substrings and values are the ending substrings.
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        str: The text with the ignored substrings removed.
    """
    for start, end in ignored_substrings.items():
        pattern: str = re.escape(start) + r'.*?' + re.escape(end)
        replacement: str = ' ' if insert_space else ''
        text = re.sub(pattern, replacement, text)  # Remove all matches of the pattern
    return text


def remove_ignored_codes(text: str, ignored_codes: list[str], insert_space: bool) -> str:
    """Remove codes of the game from the string

    Args:
        text (str): The input text.
        ignored_codes (dict[str]): A dictionary where codes to removes
        substrings and values are the ending substrings.
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        str: The text with the ignored substrings removed.
    """
    for code in ignored_codes:
        if insert_space:
            text = text.replace(code, " ")
        else:
            text = text.replace(code, "")
    return text


def save_result_process(name_file: str, method: int, data: list[tuple[int, str]]) -> None:
    folder_name: str = data_json[id_current_game - 1]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name, LIST_METHOD_FOLDER_NAME[method - 1])
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def orthocheck_load_dictionary() -> None:
    """call load_words of orthocheck
    """
    orthocheck.load_words("dictionary_orthocheck")


def orthocheck_process(url_sheet: str, column_letter: str) -> list[tuple[int, str]] | int:
    """get the list of specific words of a game in the sheet
    and call process_orthocheck of orthocheck and return result

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    error_code: int = get_list_sentence_sheet(url_sheet, column_letter, True, True)
    if error_code == 0:
        get_list_specific_word(id_current_game - 1)
        return orthocheck.process_orthocheck(list_sentences_current_sheet, list_specific_word_current_game)
    else:
        return error_code


def orthocheck_add_word_to_csv(word: str) -> None:
    """Add a word to the end of a CSV file.

    Args:
        word (str): The word to add.
        csv_file (str): The path to the CSV file.
    """
    path_csv: str = "dictionary_orthocheck\\added_words.csv"
    with open(path_csv, 'a', encoding='utf-8') as file:
        file.write(f"{word}\n")
