from datetime import datetime
import json
import os
from typing import Any
import script.utils as utils


JSON_FILE_PATH: str = "./json_data_games.json"

data_json: dict[str, Any] = {}


def load_json() -> None:
    """load json data
    """
    global data_json
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data_json = json.load(file)


def add_correct_letter(id_game: int, new_letter: str, ) -> None:
    """add a character in the json to correct_letters of the current game

    Args:
        new_letter (str): character to add
        json_file_path (str): path of the json file
    """
    if new_letter not in data_json[id_game]['correct_letters']:  # type: ignore
        data_json[id_game]['correct_letters'] += new_letter  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json, file, ensure_ascii=False, indent=4)


def add_correct_punctuation(id_game: int, new_letter: str) -> None:
    """add a punctuation in the json to correct_letters of the current game

    Args:
        new_letter (str): punctuation to add
        json_file_path (str): path of the json file
    """
    if new_letter not in data_json[id_game]['correct_punctuation']:  # type: ignore
        data_json[id_game]['correct_punctuation'] += new_letter  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json, file, ensure_ascii=False, indent=4)


def add_ignored_rules(id_game: int, rule: str) -> None:
    """add a punctuation in the json to correct_letters of the current game

    Args:
        new_letter (str): punctuation to add
        json_file_path (str): path of the json file
    """
    if rule not in data_json[id_game]['ignored_rules_languagetool']:  # type: ignore
        data_json[id_game]['ignored_rules_languagetool'].append(rule)  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json, file, ensure_ascii=False, indent=4)


def save_result_process_one_str(id_game: int, name_file: str, method: int, data: list[tuple[int, str]]) -> None:
    folder_name: str = data_json[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def save_result_process_two_str(id_game: int, name_file: str, method: int, data: list[tuple[int, str, str]]) -> None:
    folder_name: str = data_json[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_result_process(id_game: int, name_file: str) -> tuple[list[Any], list[str]]:
    result: list[list[Any]] = [[], [], []]
    modification_dates: list[str] = []
    folder_name: str = data_json[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name, name_file + ".json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            result = json.load(file)
        modification_time: float = os.path.getmtime(path)
        modification_date: str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M')
        modification_dates.append(modification_date)
    else:
        modification_dates.append("jamais lancée")
    return result, modification_dates


def remove_entry(id_game: int, name_file: str, method: int, value: str, text: str) -> None:

    print(id, name_file, method, value, text)
    folder_name: str = data_json[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    with open(os.path.join(path, name_file + ".json"), "r", encoding="utf-8") as file:
        data = json.load(file)

    value_int: int | None = utils.safe_str_to_int(value)
    if value_int is None:
        return
    data: list[str] = [entry for entry in data if entry[:2] != [value_int, text]]  # type: ignore

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
