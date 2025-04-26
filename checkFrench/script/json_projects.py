import json
from logging import Logger
from typing import TypedDict

from checkfrench.default_parameters import JSON_FILE_PATH
from checkfrench.logger import get_logger

logger: Logger = get_logger(__name__)


class Item(TypedDict):
    id: int
    title: str
    folder_name: str
    specific_argument: str
    path_dictionary: str
    valid_characters: str
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_space: dict[str, str]
    ignored_substrings_nospace: dict[str, str]
    ignored_rules_languagetool: list[str]


data_json_projects: dict[int, Item] = {}


def log_error_id_invalid(id_project: int) -> None:
    """log error if the id of the project is invalid

    Args:
        id_project (int): id of the project
    """
    logger.error(f"Project ID {id_project} is not valid.", stacklevel=2)


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


def is_id_project_valid(id_project: int) -> bool:
    """check if the id of the project is valid

    Args:
        id_project (int): id of the project

    Returns:
        bool: True if the id is valid, False otherwise
    """
    return id_project in data_json_projects


def add_valid_characters(id_project: int, characters: str) -> None:
    """add one or several characters in the json to valid_characters
    of the current project

    Args:
        id_project (int): id of the project
        characters (str): characters to add
    """
    if not is_id_project_valid(id_project):
        log_error_id_invalid(id_project)
        return
    for character in characters:
        if character not in data_json_projects[id_project]["valid_characters"]:
            data_json_projects[id_project]["valid_characters"] += character


def set_valid_characters(id_project: int, characters: str) -> None:
    """set the valid alphanumeric chars to a project

    Args:
        id_project (int): id of the project
        characters (str): characters to set
    """
    if not is_id_project_valid(id_project):
        log_error_id_invalid(id_project)
        return
    data_json_projects[id_project]["valid_characters"] = characters


def add_ignored_rules(id_project: int, rule: str) -> None:
    """add a punctuation in the json to correct_letters of the current project

    Args:
        id_project (int): id of the project
        rule (str): rule to add
    """
    if not is_id_project_valid(id_project):
        log_error_id_invalid(id_project)
        return
    if rule not in data_json_projects[id_project]["ignored_rules_languagetool"]:
        data_json_projects[id_project]["ignored_rules_languagetool"].append(rule)
