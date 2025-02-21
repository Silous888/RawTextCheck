""""main process of the application"""

# -------------------- Import Lib Standard -------------------
from datetime import datetime
import re

# -------------------- Import Lib User -------------------
from api import google_sheet_api as gsheet
from api import google_drive_api as gdrive
import json_management as json_man
import languagetool
import orthocheck
import utils
import word_check


ID_SHEET_DICT_GAME: str = "1tjUT3K4kX5_ArT6GXXovWEMf1JmeQRr6_JiqxBCSVrc"


id_current_game: int = 0
list_specific_word_current_game: list[str] = []
list_sentences_current_sheet: list[str] = []

list_specific_word_to_upload: list[str] = []

list_ignored_languagetool_rules_current_game: list[str] = []

list_ignored_languagetool_rules_current_file: list[str] = []


def get_current_date() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M')


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


def get_list_ignored_languagetool_rules() -> None:
    """get the list of ignored rules of a game in the sheet

    Returns:
        int : 0 if no problem, error code otherwise
    """
    global list_ignored_languagetool_rules_current_game
    list_ignored_languagetool_rules_current_game = json_man.data_json[
        id_current_game - 1]["ignored_rules_languagetool"]  # type: ignore


def get_index_item_with_rule(rule: str) -> list[int]:
    """get the index of the item with a specific rule in the list of ignored rules

    Args:
        rule (str): rule to find

    Returns:
        list[int] : list of index of the item with the rule
    """
    return [i for i, x in enumerate(list_ignored_languagetool_rules_current_file) if x == rule]


def remove_rule_current_file(rule: str) -> None:
    """get the index of the item with a specific rule in the list of ignored rules

    Args:
        rule (str): rule to find

    Returns:
        list[int] : list of index of the item with the rule
    """
    global list_ignored_languagetool_rules_current_file
    list_ignored_languagetool_rules_current_file = [
        x for x in list_ignored_languagetool_rules_current_file if x != rule
    ]


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
    gsheet.open_spreadsheet(utils.extract_google_drive_id(url_sheet))
    num_column: int = utils.get_position_letter_alphabet(column_letter)
    sheet_extraction: list[str] | int = gsheet.get_value_column(0, num_column)
    if isinstance(sheet_extraction, int):
        return sheet_extraction
    ignored_substrings: dict[str, str] = json_man.data_json[id_current_game - 1]["ignored_substrings"]  # type: ignore
    ignored_codes: list[str] = json_man.data_json[id_current_game - 1]["ignored_codes"]  # type: ignore
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
    print(list_specific_word_to_upload)
    get_list_specific_word(id_current_game - 1)
    list_specific_word_current_game = list_specific_word_current_game + list_specific_word_to_upload
    list_specific_word_current_game.sort()
    gsheet.open_spreadsheet(ID_SHEET_DICT_GAME)
    gsheet.set_sheet_values(id_current_game - 1, [[word] for word in list_specific_word_current_game])
    list_specific_word_to_upload.clear()


def get_name_and_type_of_url(url: str) -> tuple[str, str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: dict[str, str] | int = gdrive.get_file_metadata(utils.extract_google_drive_id(url))
        if not isinstance(output, int):
            return output["name"], output["mimeType"]
    except Exception:
        return -1
    return -2


def get_sheet_name_in_folder(url_folder: str) -> list[str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: list[list[str]] | int = gdrive.list_spreadsheet_in_folder(utils.extract_google_drive_id(url_folder))
        if not isinstance(output, int):
            return [item[0] for item in output]
    except Exception:
        return -1
    return -2


def get_sheet_url_in_folder(url_folder: str) -> list[str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: list[list[str]] | int = gdrive.list_spreadsheet_in_folder(utils.extract_google_drive_id(url_folder))
        if not isinstance(output, int):
            return [item[1] for item in output]
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


def orthocheck_load_dictionary() -> None:
    """call load_words of orthocheck
    """
    orthocheck.load_words("dictionary_orthocheck")


def language_tool_initialize() -> None:
    """call initialize_tool of languagetool
    """
    languagetool.initialize_tool()


def language_tool_close() -> None:
    """call close_tool of languagetool
    """
    languagetool.close_tool()


def orthocheck_process(url_sheet: str, column_letter: str) -> list[tuple[int, str]] | int:
    """get the list of specific words of a game in the sheet
    and call process_orthocheck of orthocheck and return result

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    error_code: int = get_list_sentence_sheet(url_sheet, column_letter, True, True)
    if error_code != 0:
        return error_code
    get_list_specific_word(id_current_game - 1)
    correct_char: str = json_man.data_json[id_current_game - 1]["correct_letters"]  # type: ignore
    correct_punct: str = json_man.data_json[id_current_game - 1]["correct_punctuation"]  # type: ignore
    return orthocheck.process_orthocheck(list_sentences_current_sheet,
                                         list_specific_word_current_game,
                                         correct_char, correct_punct)


def add_filename_to_output(url_sheet: str, output: list[tuple[int, str]]) -> list[tuple[str, int, str]] | int:
    name_sheet: str | int = gdrive.get_name_by_id(utils.extract_google_drive_id(url_sheet))
    if isinstance(name_sheet, int):
        return name_sheet
    return [(name_sheet, line[0], line[1]) for line in output]


def add_filename_to_output2(url_sheet: str, output: list[tuple[int, str]]) -> list[tuple[str, int, str, str]] | int:
    name_sheet: str | int = gdrive.get_name_by_id(utils.extract_google_drive_id(url_sheet))
    if isinstance(name_sheet, int):
        return name_sheet
    return [(name_sheet, line[0], line[1], line[2]) for line in output]  # type: ignore


def orthocheck_add_word_to_csv(word: str) -> None:
    """Add a word to the end of a CSV file.

    Args:
        word (str): The word to add.
        csv_file (str): The path to the CSV file.
    """
    path_csv: str = "dictionary_orthocheck\\added_words.csv"
    with open(path_csv, 'a', encoding='utf-8') as file:
        file.write(f"{word}\n")


def language_tool_process(url_sheet: str, column_letter: str) -> list[tuple[int, str, str]] | int:
    """get the list of specific words of a game in the sheet
    and call language_tool_on_text of languageTool and return result

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    error_code: int = get_list_sentence_sheet(url_sheet, column_letter, True, True)
    if error_code == 0:
        get_list_specific_word(id_current_game - 1)
        return languagetool.language_tool_on_text(list_sentences_current_sheet, list_specific_word_current_game,
                                                  list_ignored_languagetool_rules_current_game)
    else:
        return error_code


def word_check_process(url_sheet: str, column_letter: str) -> list[tuple[int, str]] | int:
    """get the list of specific words of a game in the sheet
    and call word_on_text of word_check and return result

    Args:
        sheet_index (int): index related to the game wanted,

    Returns:
        int : 0 if no problem, error code otherwise
    """
    error_code: int = get_list_sentence_sheet(url_sheet, column_letter, True, True)
    if error_code == 0:
        get_list_specific_word(id_current_game - 1)
        return word_check.word_on_text(list_sentences_current_sheet, list_specific_word_current_game)
    else:
        return error_code


def search_string_in_sheet(url_sheet: str, column_letter: str, string_to_search: str) -> list[tuple[int, str]] | int:
    error_code: int = get_list_sentence_sheet(url_sheet, column_letter, True, True)
    if error_code != 0:
        return error_code
    return [(i, sentence) for i, sentence in enumerate(list_sentences_current_sheet) if string_to_search in sentence]
