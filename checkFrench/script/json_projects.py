import json

from typing import TypedDict

from checkFrench.default_parameters import JSON_FILE_PATH


class Item(TypedDict):
    id: int
    title: str
    folder_name: str
    specific_argument: str
    path_dictionary: str
    valid_alphanumeric: str
    valid_punctuation: str
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_space: dict[str, str]
    ignored_substrings_nospace: dict[str, str]
    ignored_rules_languagetool: list[str]


data_json_projects: dict[int, Item] = {}


def load_json_projects() -> None:
    """load json data"""
    global data_json_projects
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data: list[Item] = json.load(file)
        data_json_projects = {item["id"]: item for item in data}


def save_json_projects() -> None:
    """save json data"""
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(list(data_json_projects.values()), file, ensure_ascii=False, indent=4)


def add_correct_alphanumeric(id_project: int, alphanumeric_chars: str, ) -> None:
    """add one or several characters in the json to valid_alphanumeric
    of the current project

    Args:
        new_alphanumeric (str): character to add
        json_file_path (str): path of the json file
    """
    for alphanumeric_char in alphanumeric_chars:
        if alphanumeric_char not in data_json_projects[id_project]["valid_alphanumeric"]:
            data_json_projects[id_project]["valid_alphanumeric"] += alphanumeric_char

    save_json_projects()


def set_valid_alphanumeric(id_project: int, alphanumeric_chars: str) -> None:
    """set the valid alphanumeric chars to a project

    Args:
        alphanumeric_chars (str): characters to set
        json_file_path (str): path of the json file
    """
    data_json_projects[id_project]["valid_alphanumeric"] = alphanumeric_chars

    save_json_projects()


def add_valid_punctuation(id_project: int, punctuation_chars: str) -> None:
    """add a punctuation in the json to valid_punctuation of the current project

    Args:
        new_letter (str): punctuation chars to add
        json_file_path (str): path of the json file
    """
    for punctuation_char in punctuation_chars:
        if punctuation_char not in data_json_projects[id_project]["valid_punctuation"]:
            data_json_projects[id_project]["valid_punctuation"] += punctuation_char

    save_json_projects()


def set_valid_punctuation(id_project: int, punctuation_chars: str) -> None:
    """set the valid punctuation chars to a project

    Args:
        punctuation_chars (str): punctuation chars to set
        json_file_path (str): path of the json file
    """
    data_json_projects[id_project]["valid_punctuation"] = punctuation_chars

    save_json_projects()


def add_ignored_rules(id_project: int, rule: str) -> None:
    """add a punctuation in the json to correct_letters of the current project

    Args:
        new_letter (str): punctuation to add
        json_file_path (str): path of the json file
    """
    if rule not in data_json_projects[id_project]["ignored_rules_languagetool"]:
        data_json_projects[id_project]["ignored_rules_languagetool"].append(rule)

    save_json_projects()
