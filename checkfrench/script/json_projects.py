"""
File        : json_projects.py
Author      : Silous
Created on  : 2025-05-19
Description : Module for managing project configuration stored in a JSON file.

This module provides functions to load, manipulate, and persist project metadata
used by the application. Each project is represented by an entry in a JSON file and
is identified by a unique name that will be used as ID.

The JSON structure is expected to follow the `Item` TypedDict definition.

Features:
- Load and save project data from/to a JSON file
- Create, update, and delete individual project entries
- Modify specific fields such as valid characters or ignored patterns
- Utility functions for managing nested lists and dictionaries within each project entry

Dependencies:
- checkfrench.default_parameters.JSON_FILE_PATH: path to the JSON configuration file
- checkfrench.logger.get_logger: logging utility
- checkfrench.newtype.Item: type definition for project items
"""


# == Imports ==================================================================

import json
from logging import Logger
import os

from checkfrench.default_parameters import CONFIG_FOLDER, JSON_PROJECT_PATH
from checkfrench.logger import get_logger
from checkfrench.newtype import ItemProject


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def log_error_id_invalid(project_name: str, stacklevel: int = 2) -> None:
    """log error if the id of the project is invalid

    Args:
        project_name (str): id of the project
        stacklevel (int): level of the stack to log the error
    """
    logger.error("Project ID %s is not valid.", project_name, stacklevel=stacklevel)


def _log_error_if_id_or_value_invalid(project_name: str, *values: str) -> bool:
    """Log an error if the project name is invalid or if any of the values are empty.
    Args:
        project_name (str): The name of the project to check.
        *values (str): Values to check for emptiness.
    Returns:
        bool: True if an error was logged, False otherwise.
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name, stacklevel=4)
        return True
    if any(value == "" for value in values):
        logger.error("Value(s) cannot be empty.", stacklevel=3)
        return True
    return False


def create_json() -> None:
    """create json for projects config if the file
    doesn't exist
    """
    if os.path.exists(JSON_PROJECT_PATH):
        return

    os.makedirs(CONFIG_FOLDER, exist_ok=True)

    with open(JSON_PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
    logger.info("Created %s.", JSON_PROJECT_PATH)


def is_project_name_exist(project_name: str) -> bool:
    """check if the id of the project is valid

    Args:
        project_name (str): id of the project

    Returns:
        bool: True if the id is valid, False otherwise
    """
    data: dict[str, ItemProject] = load_data()
    return project_name in data


def load_data() -> dict[str, ItemProject]:
    """get all data

    Returns:
        dict[str, ItemProject]: data of every projects
    """
    with open(JSON_PROJECT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, ItemProject]) -> None:
    """save data in the json, will overwrite everything
    in the file

    Args:
        data (dict[str, ItemProject]): data to save
    """
    with open(JSON_PROJECT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_projects_name() -> list[str]:
    """Get the list of project names from the JSON file.

    Returns:
        list[str]: List of project names.
    """
    data: dict[str, ItemProject] = load_data()
    return list(data.keys())


def get_project_data(project_name: str) -> ItemProject | None:
    """Get the project data for a given project name.

    Args:
        project_name (str): The name of the project to retrieve.

    Returns:
        Item | None: The project data if found, otherwise None.
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return None
    data: dict[str, ItemProject] = load_data()
    return data.get(project_name)


def create_new_entry(
        project_name: str,
        language: str,
        parser: str,
        arg_parser: str = "",
        valid_characters: str = "",
        dictionary: list[str] | None = None,
        banwords: list[str] | None = None,
        ignored_codes_into_space: list[str] | None = None,
        ignored_codes_into_nothing: list[str] | None = None,
        ignored_substrings_into_space: dict[str, list[str]] | None = None,
        ignored_substrings_into_nothing: dict[str, list[str]] | None = None,
        ignored_rules: list[str] | None = None,
        synchronized_path: str = ""
        ) -> None:
    """Add a new entry in the json

    Args:
        project_name (str): need to be specified and must be unique
        language (str): need to be specified
        parser (str, optional): need to be specified
        arg_parser (str, optional): Defaults to "".
        valid_characters (str, optional): Defaults to "".
        dictionary (list[str], optional): Defaults to [].
        banwords (list[str], optional): Defaults to [].
        ignored_codes_into_space (list[str], optional): Defaults to [].
        ignored_codes_into_nothing (list[str], optional): Defaults to [].
        ignored_substrings_into_space (dict[str, list[str]], optional): Defaults to {}.
        ignored_substrings_into_nothing (dict[str, list[str]], optional): Defaults to {}.
        ignored_rules (list[str], optional): Defaults to [].

    Returns:
        int: Id of the entry created
    """
    if not project_name:
        logger.error("Project name cannot be empty.")
        return
    if not language:
        logger.error("Language cannot be empty.")
        return
    if not parser:
        logger.error("Parser cannot be empty.")

    data: dict[str, ItemProject] = load_data()

    if project_name in data:
        logger.error("Project name already exists: %s", project_name)
        return

    data[project_name] = {
        "language": language,
        "parser": parser,
        "arg_parser": arg_parser,
        "valid_characters": valid_characters,
        "dictionary": dictionary or [],
        "banwords": banwords or [],
        "ignored_codes_into_space": ignored_codes_into_space or [],
        "ignored_codes_into_nothing": ignored_codes_into_nothing or [],
        "ignored_substrings_into_space": ignored_substrings_into_space or {},
        "ignored_substrings_into_nothing": ignored_substrings_into_nothing or {},
        "ignored_rules": ignored_rules or [],
        "synchronized_path": synchronized_path
    }

    save_data(data)
    logger.info("Project '%s' created.", project_name)


def set_entry(
    project_name: str,
    language: str | None = None,
    parser: str | None = None,
    arg_parser: str | None = None,
    valid_characters: str | None = None,
    dictionary: list[str] | None = None,
    banwords: list[str] | None = None,
    ignored_codes_into_space: list[str] | None = None,
    ignored_codes_into_nothing: list[str] | None = None,
    ignored_substrings_into_space: dict[str, list[str]] | None = None,
    ignored_substrings_into_nothing: dict[str, list[str]] | None = None,
    ignored_rules: list[str] | None = None,
    synchronized_path: str | None = None
) -> None:
    """set the entry in the json, if arg not specified, it will not be changed
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    if language is not None:
        set_language(project_name, language)
    if parser is not None:
        set_parser(project_name, parser)
    if arg_parser is not None:
        set_arg_parser(project_name, arg_parser)
    if valid_characters is not None:
        set_valid_characters(project_name, valid_characters)
    if dictionary is not None:
        set_dictionary_words(project_name, dictionary)
    if banwords is not None:
        set_banwords(project_name, banwords)
    if ignored_codes_into_space is not None:
        set_ignored_codes_into_space(project_name, ignored_codes_into_space)
    if ignored_codes_into_nothing is not None:
        set_ignored_codes_into_nothing(project_name, ignored_codes_into_nothing)
    if ignored_substrings_into_space is not None:
        set_ignored_substrings_into_space(project_name, ignored_substrings_into_space)
    if ignored_substrings_into_nothing is not None:
        set_ignored_substrings_into_nothing(project_name, ignored_substrings_into_nothing)
    if ignored_rules is not None:
        set_ignored_rules(project_name, ignored_rules)
    if synchronized_path is not None:
        set_synchronized_path(project_name, synchronized_path)
    logger.info("Entry %s updated.", project_name)
    return


def set_entry_from_item(project_name: str, data: ItemProject) -> None:
    """set the entry in the json with a complete Item
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    if "language" not in data or data["language"] == "":
        logger.error("Language cannot be empty.")
        return
    if "parser" not in data or data["parser"] == "":
        logger.error("Parser cannot be empty.")
        return
    set_entry(
        project_name,
        language=data["language"],
        parser=data["parser"],
        arg_parser=data["arg_parser"],
        valid_characters=data["valid_characters"],
        dictionary=data["dictionary"],
        banwords=data["banwords"],
        ignored_codes_into_space=data["ignored_codes_into_space"],
        ignored_codes_into_nothing=data["ignored_codes_into_nothing"],
        ignored_substrings_into_space=data["ignored_substrings_into_space"],
        ignored_substrings_into_nothing=data["ignored_substrings_into_nothing"],
        ignored_rules=data["ignored_rules"],
        synchronized_path=data["synchronized_path"]
    )


def delete_entry(project_name: str) -> None:
    """delete entry by id
    Args:
        project_name (str): id of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    if project_name not in data:
        return
    del data[project_name]
    save_data(data)
    logger.info("Entry %s deleted.", project_name)
    return


def set_new_project_name(project_name: str, new_project_name: str) -> None:
    """set the new project_name of the project

    Args:
        project_name (str): id of the project
        new_project_name (str): new project_name of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    if new_project_name == "":
        logger.error("project_name cannot be empty.")
        return
    data: dict[str, ItemProject] = load_data()
    data[new_project_name] = data[project_name]
    del data[project_name]
    save_data(data)


def set_language(project_name: str, language: str) -> None:
    """set the language of the project

    Args:
        project_name (str): id of the project
        language (str): language of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    if language == "":
        logger.error("Language cannot be empty.")
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name]["language"] = language
    save_data(data)


def set_parser(project_name: str, parser: str) -> None:
    """set the parser of the project

    Args:
        project_name (str): id of the project
        parser (str): parser of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    if parser == "":
        logger.error("Parser cannot be empty.")
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name]["parser"] = parser
    save_data(data)


def set_arg_parser(project_name: str, specific_argument: str) -> None:
    """set the specific argument of the project

    Args:
        project_name (str): id of the project
        specific_argument (str): specific argument of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name]["arg_parser"] = specific_argument
    save_data(data)


def set_valid_characters(project_name: str, characters: str) -> None:
    """set the valid alphanumeric chars to a project

    Args:
        project_name (str): id of the project
        characters (str): characters to set
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name]["valid_characters"] = characters
    save_data(data)


def add_valid_characters(project_name: str, characters: str) -> None:
    """add one or several characters in the json to valid_characters

    Args:
        project_name (str): id of the project
        characters (str): characters to add
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    for character in characters:
        if character not in data[project_name]["valid_characters"]:
            data[project_name]["valid_characters"] += character
    save_data(data)


def set_dictionary_words(project_name: str, dictionary_words: list[str]) -> None:
    """set the dictionary_words of the project

    Args:
        project_name (str): id of the project
        dictionary_words (list[str]): dictionary words to set
    """
    _set_to_list_field(project_name, "dictionary", dictionary_words)


def add_dictionary_word(project_name: str, dictionary_word: str) -> None:
    """add a word to the dictionary of the project

    Args:
        project_name (str): id of the project
        dictionary_word (str): word to add
    """
    _add_to_list_field(project_name, "dictionary", dictionary_word)


def remove_dictionary_word(project_name: str, dictionary_word: str) -> None:
    """remove a word to the dictionary of the project

    Args:
        project_name (str): id of the project
        dictionary_word (str): word to remove
    """
    _remove_from_list_field(project_name, "dictionary", dictionary_word)


def set_banwords(project_name: str, banwords: list[str]) -> None:
    """set the banwords of the project

    Args:
        project_name (str): id of the project
        banwords (list[str]): banwords to set
    """
    _set_to_list_field(project_name, "banwords", banwords)


def add_banword(project_name: str, banword: str) -> None:
    """add a banword to the project

    Args:
        project_name (str): id of the project
        banword (str): banword to add
    """
    _add_to_list_field(project_name, "banwords", banword)


def remove_banword(project_name: str, banword: str) -> None:
    """remove a banword from the project

    Args:
        project_name (str): id of the project
        banword (str): banword to remove
    """
    _remove_from_list_field(project_name, "banwords", banword)


def set_ignored_codes_into_space(project_name: str, codes: list[str]) -> None:
    """set the ignored codes into space of the project

    Args:
        project_name (str): id of the project
        codes (list[str]): codes to set
    """
    _set_to_list_field(project_name, "ignored_codes_into_space", codes)


def add_ignored_codes_into_space(project_name: str, code: str) -> None:
    """add a code to the ignored codes into space of the project
    Args:
        project_name (str): id of the project
        code (str): code to add
    """
    _add_to_list_field(project_name, "ignored_codes_into_space", code)


def remove_ignored_codes_into_space(project_name: str, code: str) -> None:
    """remove a code from the ignored codes into space of the project
    Args:
        project_name (str): id of the project
        code (str): code to remove
    """
    _remove_from_list_field(project_name, "ignored_codes_into_space", code)


def set_ignored_codes_into_nothing(project_name: str, codes: list[str]) -> None:
    """set the ignored codes into nothing of the project

    Args:
        project_name (str): id of the project
        codes (list[str]): codes to set
    """
    _set_to_list_field(project_name, "ignored_codes_into_nothing", codes)


def add_ignored_codes_into_nothing(project_name: str, code: str) -> None:
    """add a code to the ignored codes into nothing of the project
    Args:
        project_name (str): id of the project
        code (str): code to add
    """
    _add_to_list_field(project_name, "ignored_codes_into_nothing", code)


def remove_ignored_codes_into_nothing(project_name: str, code: str) -> None:
    """remove a code from the ignored codes into nothing of the project
    Args:
        project_name (str): id of the project
        code (str): code to remove
    """
    _remove_from_list_field(project_name, "ignored_codes_into_nothing", code)


def set_ignored_substrings_into_space(project_name: str, substrings: dict[str, list[str]]) -> None:
    """set the ignored substrings into space of the project

    Args:
        project_name (str): id of the project
        substrings (dict[str, list[str]]): substrings to set
    """
    _set_to_dict_list_field(project_name, "ignored_substrings_into_space", substrings)


def add_ignored_substrings_into_space(project_name: str, begin: str, end: str) -> None:
    """add a substring to the ignored substrings into space of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _add_to_dict_list_field(project_name, "ignored_substrings_into_space", begin, end)


def remove_ignored_substrings_into_space(project_name: str, begin: str, end: str) -> None:
    """remove a substring from the ignored substrings into space of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _remove_from_dict_list_field(project_name, "ignored_substrings_into_space", begin, end)


def set_ignored_substrings_into_nothing(project_name: str, substrings: dict[str, list[str]]) -> None:
    """set the ignored substrings into nothing of the project

    Args:
        project_name (str): id of the project
        substrings (dict[str, list[str]]): substrings to set
    """
    _set_to_dict_list_field(project_name, "ignored_substrings_into_nothing", substrings)


def add_ignored_substrings_into_nothing(project_name: str, begin: str, end: str) -> None:
    """add a substring to the ignored substrings into nothing of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _add_to_dict_list_field(project_name, "ignored_substrings_into_nothing", begin, end)


def remove_ignored_substrings_into_nothing(project_name: str, begin: str, end: str) -> None:
    """remove a substring from the ignored substrings into nothing of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _remove_from_dict_list_field(project_name, "ignored_substrings_into_nothing", begin, end)


def set_ignored_rules(project_name: str, rules: list[str]) -> None:
    """set the ignored rules of the project

    Args:
        project_name (str): id of the project
        rules (list[str]): rules to set
    """
    _set_to_list_field(project_name, "ignored_rules", rules)


def add_ignored_rules(project_name: str, rule: str) -> None:
    """add a rule to the ignored rules of the project
    Args:
        project_name (str): id of the project
        rule (str): rule to add
    """
    _add_to_list_field(project_name, "ignored_rules", rule)


def remove_ignored_rules(project_name: str, rule: str) -> None:
    """remove a rule from the ignored rules of the project
    Args:
        project_name (str): id of the project
        rule (str): rule to remove
    """
    _remove_from_list_field(project_name, "ignored_rules", rule)


def set_synchronized_path(project_name: str, path: str) -> None:
    """set the synchronized path of the project

    Args:
        project_name (str): id of the project
        path (str): path for synchronizing the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name]["synchronized_path"] = path
    save_data(data)


# ------------------------------Internal utility functions---------------------


def _set_to_list_field(project_name: str, field: str, values: list[str]) -> None:
    """Set the field to a new list of values"""
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name][field] = values
    save_data(data)


def _add_to_list_field(project_name: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, value):
        return
    data: dict[str, ItemProject] = load_data()
    if value not in data[project_name][field]:
        data[project_name][field].append(value)  # type: ignore
        save_data(data)


def _remove_from_list_field(project_name: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, value):
        return
    data: dict[str, ItemProject] = load_data()
    if value in data[project_name][field]:
        data[project_name][field].remove(value)  # type: ignore
        save_data(data)


def _set_to_dict_list_field(project_name: str, field: str, values: dict[str, list[str]]) -> None:
    """Set the field to a new dictionary of lists"""
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, ItemProject] = load_data()
    data[project_name][field] = values
    save_data(data)


def _add_to_dict_list_field(project_name: str, field: str, key: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, key, value):
        return
    data: dict[str, ItemProject] = load_data()
    if key not in data[project_name][field]:
        data[project_name][field][key] = []
    if value not in data[project_name][field][key]:
        data[project_name][field][key].append(value)  # type: ignore
    save_data(data)


def _remove_from_dict_list_field(
    project_name: str, field: str, key: str, value: str
) -> None:
    if _log_error_if_id_or_value_invalid(project_name, key, value):
        return
    data: dict[str, ItemProject] = load_data()
    if key in data[project_name][field]:
        if value in data[project_name][field][key]:
            data[project_name][field][key].remove(value)  # type: ignore
        if not data[project_name][field][key]:
            del data[project_name][field][key]
    save_data(data)
