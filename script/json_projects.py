import json

from typing import TypedDict


class Item(TypedDict):
    id: int
    title: str
    folder_name: str
    specific_argument: str
    path_dictionary: str
    valid_letters: str
    valid_punctuation: str
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_space: dict[str, str]
    ignored_substrings_nospace: dict[str, str]
    ignored_rules_languagetool: list[str]


JSON_FILE_PATH: str = "./json_data_projects.json"

data_json_projects: dict[int, Item] = {}


def load_json_projects() -> None:
    """load json data
    """
    global data_json_projects
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data: list[Item] = json.load(file)
        data_json_projects = {item["id"]: item for item in data}


def add_correct_letter(id_game: int, new_letter: str, ) -> None:
    """add a character in the json to correct_letters of the current game

    Args:
        new_letter (str): character to add
        json_file_path (str): path of the json file
    """
    if new_letter not in data_json_projects[id_game]['correct_letters']:  # type: ignore
        data_json_projects[id_game]['correct_letters'] += new_letter  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json_projects, file, ensure_ascii=False, indent=4)


def add_correct_punctuation(id_game: int, new_letter: str) -> None:
    """add a punctuation in the json to correct_letters of the current game

    Args:
        new_letter (str): punctuation to add
        json_file_path (str): path of the json file
    """
    if new_letter not in data_json_projects[id_game]['correct_punctuation']:  # type: ignore
        data_json_projects[id_game]['correct_punctuation'] += new_letter  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json_projects, file, ensure_ascii=False, indent=4)


def add_ignored_rules(id_game: int, rule: str) -> None:
    """add a punctuation in the json to correct_letters of the current game

    Args:
        new_letter (str): punctuation to add
        json_file_path (str): path of the json file
    """
    if rule not in data_json_projects[id_game]['ignored_rules_languagetool']:  # type: ignore
        data_json_projects[id_game]['ignored_rules_languagetool'].append(rule)  # type: ignore

    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data_json_projects, file, ensure_ascii=False, indent=4)
