import json
from logging import Logger
from typing import TypedDict

from checkfrench.default_parameters import JSON_FILE_PATH
from checkfrench.logger import get_logger
from checkfrench.script.utils import sanitize_folder_name

logger: Logger = get_logger(__name__)


class Item(TypedDict):
    id: int
    title: str
    specific_argument: str
    path_dictionary: str
    valid_characters: str
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_space: dict[str, list[str]]
    ignored_substrings_nospace: dict[str, list[str]]
    ignored_rules_languagetool: list[str]


data_json_projects: dict[int, Item] = {}


def log_error_id_invalid(id_project: int, stacklevel: int = 2) -> None:
    """log error if the id of the project is invalid

    Args:
        id_project (int): id of the project
    """
    logger.error("Project ID %s is not valid.", id_project, stacklevel=stacklevel)


def _log_error_if_id_or_value_invalid(id_project: int, *values: str) -> bool:
    """Internal function to log error and return True if any value is invalid"""
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project, stacklevel=4)
        return True
    if any(value == "" for value in values):
        logger.error("Value(s) cannot be empty.", stacklevel=3)
        return True
    return False


def is_id_project_exist(id_project: int) -> bool:
    """check if the id of the project is valid

    Args:
        id_project (int): id of the project

    Returns:
        bool: True if the id is valid, False otherwise
    """
    return id_project in data_json_projects


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


def create_new_entry(
    title: str,
    specific_argument: str = "",
    path_dictionary: str = "",
    valid_characters: str = "",
    ignored_codes_into_space: list[str] | None = None,
    ignored_codes_into_nospace: list[str] | None = None,
    ignored_substrings_space: dict[str, list[str]] | None = None,
    ignored_substrings_nospace: dict[str, list[str]] | None = None,
    ignored_rules_languagetool: list[str] | None = None,
) -> int:
    """Add a new entry in the json

    Args:
        title (str): need to be specified
        specific_argument (str, optional): Defaults to "".
        path_dictionary (str, optional): Defaults to "".
        valid_characters (str, optional): Defaults to "".
        ignored_codes_into_space (list[str], optional): Defaults to [].
        ignored_codes_into_nospace (list[str], optional): Defaults to [].
        ignored_substrings_space (dict[str, list[str]], optional): Defaults to {}.
        ignored_substrings_nospace (dict[str, list[str]], optional): Defaults to {}.
        ignored_rules_languagetool (list[str], optional): Defaults to [].

    Returns:
        int: Id of the entry created
    """
    #TODO
    return 0

def set_entry(
    id_project: int,
    title: str,
    specific_argument: str = "",
    path_dictionary: str = "",
    valid_characters: str = "",
    ignored_codes_into_space: list[str] | None = None,
    ignored_codes_into_nospace: list[str] | None = None,
    ignored_substrings_space: dict[str, list[str]] | None = None,
    ignored_substrings_nospace: dict[str, list[str]] | None = None,
    ignored_rules_languagetool: list[str] | None = None,
) -> None:
    #TODO
    return


def delete_entry(id: int) -> None:
    """delete entry by id
    """
    #TODO
    return


def create_id() -> int:
    """Create a new id not used

    Returns:
        int: id for a new entry
    """
    #TODO
    return 0


def set_title(id_project: int, title: str) -> None:
    """set the title of the project

    Args:
        id_project (int): id of the project
        title (str): title of the project
    """
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project)
        return
    if title == "":
        logger.error("Title cannot be empty.")
        return
    data_json_projects[id_project]["title"] = title


def set_specific_argument(id_project: int, specific_argument: str) -> None:
    """set the specific argument of the project

    Args:
        id_project (int): id of the project
        specific_argument (str): specific argument of the project
    """
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project)
        return
    data_json_projects[id_project]["specific_argument"] = specific_argument


def set_path_dictionary(id_project: int, path_dictionary: str) -> None:
    """set the path of the dictionary of the project

    Args:
        id_project (int): id of the project
        path_dictionary (str): path of the dictionary of the project
    """
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project)
        return
    data_json_projects[id_project]["path_dictionary"] = path_dictionary


def add_valid_characters(id_project: int, characters: str) -> None:
    """add one or several characters in the json to valid_characters

    Args:
        id_project (int): id of the project
        characters (str): characters to add
    """
    if not is_id_project_exist(id_project):
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
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project)
        return
    data_json_projects[id_project]["valid_characters"] = characters


def add_ignored_codes_into_space(id_project: int, code: str) -> None:
    _add_to_list_field(id_project, "ignored_codes_into_space", code)


def remove_ignored_codes_into_space(id_project: int, code: str) -> None:
    _remove_from_list_field(id_project, "ignored_codes_into_space", code)


def add_ignored_codes_into_nospace(id_project: int, code: str) -> None:
    _add_to_list_field(id_project, "ignored_codes_into_nospace", code)


def remove_ignored_codes_into_nospace(id_project: int, code: str) -> None:
    _remove_from_list_field(id_project, "ignored_codes_into_nospace", code)


def add_ignored_substrings_space(id_project: int, begin: str, end: str) -> None:
    _add_to_dict_list_field(id_project, "ignored_substrings_space", begin, end)


def remove_ignored_substrings_space(id_project: int, begin: str, end: str) -> None:
    _remove_from_dict_list_field(id_project, "ignored_substrings_space", begin, end)


def add_ignored_substrings_nospace(id_project: int, begin: str, end: str) -> None:
    _add_to_dict_list_field(id_project, "ignored_substrings_nospace", begin, end)


def remove_ignored_substrings_nospace(id_project: int, begin: str, end: str) -> None:
    _remove_from_dict_list_field(id_project, "ignored_substrings_nospace", begin, end)


def add_ignored_rules(id_project: int, rule: str) -> None:
    _add_to_list_field(id_project, "ignored_rules_languagetool", rule)


def remove_ignored_rules(id_project: int, rule: str) -> None:
    _remove_from_list_field(id_project, "ignored_rules_languagetool", rule)


def get_folder_result(id_project: int) -> str | int:
    """get the folder name where results will be put

    Args:
        id_project (int): id of the project

    Returns:
        str: folder name of the project
    """
    if not is_id_project_exist(id_project):
        log_error_id_invalid(id_project)
        return 1
    return (
        str(id_project)
        + "-"
        + sanitize_folder_name(data_json_projects[id_project]["title"])
    )


def _add_to_list_field(id_project: int, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(id_project, value):
        return
    if value not in data_json_projects[id_project][field]:
        data_json_projects[id_project][field].append(value)  # type: ignore


def _remove_from_list_field(id_project: int, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(id_project, value):
        return
    if value in data_json_projects[id_project][field]:
        data_json_projects[id_project][field].remove(value)  # type: ignore


def _add_to_dict_list_field(id_project: int, field: str, key: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(id_project, key, value):
        return
    if key not in data_json_projects[id_project][field]:
        data_json_projects[id_project][field][key] = []
    if value not in data_json_projects[id_project][field][key]:
        data_json_projects[id_project][field][key].append(value)  # type: ignore


def _remove_from_dict_list_field(
    id_project: int, field: str, key: str, value: str
) -> None:
    if _log_error_if_id_or_value_invalid(id_project, key, value):
        return
    if key in data_json_projects[id_project][field]:
        if value in data_json_projects[id_project][field][key]:
            data_json_projects[id_project][field][key].remove(value)  # type: ignore
        if not data_json_projects[id_project][field][key]:
            del data_json_projects[id_project][field][key]
