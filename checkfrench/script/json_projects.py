"""
Module for managing project configuration stored in a JSON file.

This module provides functions to load, manipulate, and persist project metadata
used by the application. Each project is represented by an entry in a JSON file and
is identified by a unique title that will be used as ID.

The JSON structure is expected to follow the `Item` TypedDict definition.

Features:
- Load and save project data from/to a JSON file
- Create, update, and delete individual project entries
- Modify specific fields such as valid characters or ignored patterns
- Utility functions for managing nested lists and dictionaries within each project entry

Dependencies:
- checkfrench.default_parameters.JSON_FILE_PATH: path to the JSON configuration file
- checkfrench.logger.get_logger: logging utility

"""


import json
from logging import Logger
from typing import TypedDict

from checkfrench.default_parameters import JSON_FILE_PATH
from checkfrench.logger import get_logger

logger: Logger = get_logger(__name__)


class Item(TypedDict):

    # title_project: str as key
    language: str
    parser: str
    specific_argument: str
    path_dictionary: str
    valid_characters: str
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_space: dict[str, list[str]]
    ignored_substrings_nospace: dict[str, list[str]]
    ignored_rules_languagetool: list[str]


def log_error_id_invalid(title_project: str, stacklevel: int = 2) -> None:
    """log error if the id of the project is invalid

    Args:
        title_project (int): id of the project
    """
    logger.error("Project ID %s is not valid.", title_project, stacklevel=stacklevel)


def _log_error_if_id_or_value_invalid(title_project: str, *values: str) -> bool:
    """Internal function to log error and return True if any value is invalid"""
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project, stacklevel=4)
        return True
    if any(value == "" for value in values):
        logger.error("Value(s) cannot be empty.", stacklevel=3)
        return True
    return False


def is_title_project_exist(title_project: str) -> bool:
    """check if the id of the project is valid

    Args:
        title_project (str): id of the project

    Returns:
        bool: True if the id is valid, False otherwise
    """
    data: dict[str, Item] = load_data()
    return title_project in data


def load_data() -> dict[str, Item]:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, Item]) -> None:
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_new_entry(
        title: str,
        language: str,
        parser: str = "",
        specific_argument: str = "",
        path_dictionary: str = "",
        valid_characters: str = "",
        ignored_codes_into_space: list[str] | None = None,
        ignored_codes_into_nospace: list[str] | None = None,
        ignored_substrings_space: dict[str, list[str]] | None = None,
        ignored_substrings_nospace: dict[str, list[str]] | None = None,
        ignored_rules_languagetool: list[str] | None = None
        ) -> None:
    """Add a new entry in the json

    Args:
        title (str): need to be specified and must be unique
        language (str): need to be specified
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
    if not title:
        logger.error("Title cannot be empty.")
        raise ValueError
    if not language:
        logger.error("Language cannot be empty.")
        raise ValueError

    data: dict[str, Item] = load_data()

    if title in data:
        logger.error("Project title already exists: %s", title)
        raise ValueError

    data[title] = {
        "language": language,
        "parser": parser,
        "specific_argument": specific_argument,
        "path_dictionary": path_dictionary,
        "valid_characters": valid_characters,
        "ignored_codes_into_space": ignored_codes_into_space or [],
        "ignored_codes_into_nospace": ignored_codes_into_nospace or [],
        "ignored_substrings_space": ignored_substrings_space or {},
        "ignored_substrings_nospace": ignored_substrings_nospace or {},
        "ignored_rules_languagetool": ignored_rules_languagetool or [],
    }

    save_data(data)
    logger.info("Project '%s' created.", title)


def set_entry(
    title_project: str,
    language: str | None = None,
    parser: str | None = None,
    specific_argument: str | None = None,
    path_dictionary: str | None = None,
    valid_characters: str | None = None,
    ignored_codes_into_space: list[str] | None = None,
    ignored_codes_into_nospace: list[str] | None = None,
    ignored_substrings_space: dict[str, list[str]] | None = None,
    ignored_substrings_nospace: dict[str, list[str]] | None = None,
    ignored_rules_languagetool: list[str] | None = None,
) -> None:
    """set the entry in the json, if arg not specified, it will not be changed
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        raise ValueError
    if language is not None:
        set_language(title_project, language)
    if parser is not None:
        set_parser(title_project, parser)
    if specific_argument is not None:
        set_specific_argument(title_project, specific_argument)
    if path_dictionary is not None:
        set_path_dictionary(title_project, path_dictionary)
    if valid_characters is not None:
        set_valid_characters(title_project, valid_characters)
    if ignored_codes_into_space is not None:
        set_ignored_codes_into_space(title_project, ignored_codes_into_space)
    if ignored_codes_into_nospace is not None:
        set_ignored_codes_into_nospace(title_project, ignored_codes_into_nospace)
    if ignored_substrings_space is not None:
        set_ignored_substrings_space(title_project, ignored_substrings_space)
    if ignored_substrings_nospace is not None:
        set_ignored_substrings_nospace(title_project, ignored_substrings_nospace)
    if ignored_rules_languagetool is not None:
        set_ignored_rules(title_project, ignored_rules_languagetool)
    logger.info("Entry %s updated.", title_project)
    return


def delete_entry(title_project: str) -> None:
    """delete entry by id
    Args:
        title_project (str): id of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    if title_project not in data:
        return
    del data[title_project]
    save_data(data)
    logger.info("Entry %s deleted.", title_project)
    return


def set_new_title(title_project: str, new_title: str) -> None:
    """set the new title of the project

    Args:
        title_project (str): id of the project
        new_title (str): new title of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        raise ValueError
    if new_title == "":
        logger.error("Title cannot be empty.")
        raise ValueError
    data: dict[str, Item] = load_data()
    data[new_title] = data[title_project]
    del data[title_project]
    save_data(data)


def set_language(title_project: str, language: str) -> None:
    """set the language of the project

    Args:
        title_project (str): id of the project
        language (str): language of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        raise ValueError
    if language == "":
        logger.error("Language cannot be empty.")
        raise ValueError
    data: dict[str, Item] = load_data()
    data[title_project]["language"] = language
    save_data(data)


def set_parser(title_project: str, parser: str) -> None:
    """set the parser of the project

    Args:
        title_project (str): id of the project
        parser (str): parser of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    if parser == "":
        logger.error("Parser cannot be empty.")
        raise ValueError
    data: dict[str, Item] = load_data()
    data[title_project]["parser"] = parser
    save_data(data)


def set_specific_argument(title_project: str, specific_argument: str) -> None:
    """set the specific argument of the project

    Args:
        title_project (str): id of the project
        specific_argument (str): specific argument of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        raise ValueError
    data: dict[str, Item] = load_data()
    data[title_project]["specific_argument"] = specific_argument
    save_data(data)


def set_path_dictionary(title_project: str, path_dictionary: str) -> None:
    """set the path of the dictionary of the project

    Args:
        title_project (str): id of the project
        path_dictionary (str): path of the dictionary of the project
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["path_dictionary"] = path_dictionary
    save_data(data)


def add_valid_characters(title_project: str, characters: str) -> None:
    """add one or several characters in the json to valid_characters

    Args:
        title_project (str): id of the project
        characters (str): characters to add
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    for character in characters:
        if character not in data[title_project]["valid_characters"]:
            data[title_project]["valid_characters"] += character
    save_data(data)


def set_valid_characters(title_project: str, characters: str) -> None:
    """set the valid alphanumeric chars to a project

    Args:
        title_project (str): id of the project
        characters (str): characters to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["valid_characters"] = characters
    save_data(data)


def set_ignored_codes_into_space(title_project: str, codes: list[str]) -> None:
    """set the ignored codes into space of the project

    Args:
        title_project (str): id of the project
        codes (list[str]): codes to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["ignored_codes_into_space"] = codes
    save_data(data)


def add_ignored_codes_into_space(title_project: str, code: str) -> None:
    _add_to_list_field(title_project, "ignored_codes_into_space", code)


def remove_ignored_codes_into_space(title_project: str, code: str) -> None:
    _remove_from_list_field(title_project, "ignored_codes_into_space", code)


def set_ignored_codes_into_nospace(title_project: str, codes: list[str]) -> None:
    """set the ignored codes into nospace of the project

    Args:
        title_project (str): id of the project
        codes (list[str]): codes to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["ignored_codes_into_nospace"] = codes
    save_data(data)


def add_ignored_codes_into_nospace(title_project: str, code: str) -> None:
    _add_to_list_field(title_project, "ignored_codes_into_nospace", code)


def remove_ignored_codes_into_nospace(title_project: str, code: str) -> None:
    _remove_from_list_field(title_project, "ignored_codes_into_nospace", code)


def set_ignored_substrings_space(title_project: str, substrings: dict[str, list[str]]) -> None:
    """set the ignored substrings into space of the project

    Args:
        title_project (str): id of the project
        substrings (dict[str, list[str]]): substrings to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["ignored_substrings_space"] = substrings
    save_data(data)


def add_ignored_substrings_space(title_project: str, begin: str, end: str) -> None:
    _add_to_dict_list_field(title_project, "ignored_substrings_space", begin, end)


def remove_ignored_substrings_space(title_project: str, begin: str, end: str) -> None:
    _remove_from_dict_list_field(title_project, "ignored_substrings_space", begin, end)


def set_ignored_substrings_nospace(title_project: str, substrings: dict[str, list[str]]) -> None:
    """set the ignored substrings into nospace of the project

    Args:
        title_project (str): id of the project
        substrings (dict[str, list[str]]): substrings to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["ignored_substrings_nospace"] = substrings
    save_data(data)


def add_ignored_substrings_nospace(title_project: str, begin: str, end: str) -> None:
    _add_to_dict_list_field(title_project, "ignored_substrings_nospace", begin, end)


def remove_ignored_substrings_nospace(title_project: str, begin: str, end: str) -> None:
    _remove_from_dict_list_field(title_project, "ignored_substrings_nospace", begin, end)


def set_ignored_rules(title_project: str, rules: list[str]) -> None:
    """set the ignored rules of the project

    Args:
        title_project (str): id of the project
        rules (list[str]): rules to set
    """
    if not is_title_project_exist(title_project):
        log_error_id_invalid(title_project)
        return
    data: dict[str, Item] = load_data()
    data[title_project]["ignored_rules_languagetool"] = rules
    save_data(data)


def add_ignored_rules(title_project: str, rule: str) -> None:
    _add_to_list_field(title_project, "ignored_rules_languagetool", rule)


def remove_ignored_rules(title_project: str, rule: str) -> None:
    _remove_from_list_field(title_project, "ignored_rules_languagetool", rule)


def _add_to_list_field(title_project: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(title_project, value):
        return
    data: dict[str, Item] = load_data()
    if value not in data[title_project][field]:
        data[title_project][field].append(value)  # type: ignore
        save_data(data)


def _remove_from_list_field(title_project: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(title_project, value):
        return
    data: dict[str, Item] = load_data()
    if value in data[title_project][field]:
        data[title_project][field].remove(value)  # type: ignore
        save_data(data)


def _add_to_dict_list_field(title_project: str, field: str, key: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(title_project, key, value):
        return
    data: dict[str, Item] = load_data()
    if key not in data[title_project][field]:
        data[title_project][field][key] = []
    if value not in data[title_project][field][key]:
        data[title_project][field][key].append(value)  # type: ignore
    save_data(data)


def _remove_from_dict_list_field(
    title_project: str, field: str, key: str, value: str
) -> None:
    if _log_error_if_id_or_value_invalid(title_project, key, value):
        return
    data: dict[str, Item] = load_data()
    if key in data[title_project][field]:
        if value in data[title_project][field][key]:
            data[title_project][field][key].remove(value)  # type: ignore
        if not data[title_project][field][key]:
            del data[title_project][field][key]
    save_data(data)
