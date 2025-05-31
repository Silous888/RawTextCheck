"""
Module for managing project configuration stored in a JSON file.

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


import json
from logging import Logger


from checkfrench.default_parameters import JSON_FILE_PATH
from checkfrench.logger import get_logger
from checkfrench.newtype import Item

logger: Logger = get_logger(__name__)


def log_error_id_invalid(project_name: str, stacklevel: int = 2) -> None:
    """log error if the id of the project is invalid

    Args:
        project_name (int): id of the project
    """
    logger.error("Project ID %s is not valid.", project_name, stacklevel=stacklevel)


def _log_error_if_id_or_value_invalid(project_name: str, *values: str) -> bool:
    """Internal function to log error and return True if any value is invalid"""
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name, stacklevel=4)
        return True
    if any(value == "" for value in values):
        logger.error("Value(s) cannot be empty.", stacklevel=3)
        return True
    return False


def is_project_name_exist(project_name: str) -> bool:
    """check if the id of the project is valid

    Args:
        project_name (str): id of the project

    Returns:
        bool: True if the id is valid, False otherwise
    """
    data: dict[str, Item] = load_data()
    return project_name in data


def load_data() -> dict[str, Item]:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, Item]) -> None:
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_projects_name() -> list[str]:
    """Get the list of project names from the JSON file.

    Returns:
        list[str]: List of project names.
    """
    data: dict[str, Item] = load_data()
    return list(data.keys())


def get_project_data(project_name: str) -> Item | None:
    """Get the project data for a given project name.

    Args:
        project_name (str): The name of the project to retrieve.

    Returns:
        Item | None: The project data if found, otherwise None.
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return None
    data: dict[str, Item] = load_data()
    return data.get(project_name)


def create_new_entry(
        project_name: str,
        language: str,
        parser: str = "",
        specific_argument: str = "",
        path_dictionary: str = "",
        valid_characters: str = "",
        banwords: list[str] | None = None,
        ignored_codes_into_space: list[str] | None = None,
        ignored_codes_into_nospace: list[str] | None = None,
        ignored_substrings_into_space: dict[str, list[str]] | None = None,
        ignored_substrings_into_nospace: dict[str, list[str]] | None = None,
        ignored_rules_languagetool: list[str] | None = None
        ) -> None:
    """Add a new entry in the json

    Args:
        project_name (str): need to be specified and must be unique
        language (str): need to be specified
        specific_argument (str, optional): Defaults to "".
        path_dictionary (str, optional): Defaults to "".
        valid_characters (str, optional): Defaults to "".
        banwords (list[str], optional): Defaults to [].
        ignored_codes_into_space (list[str], optional): Defaults to [].
        ignored_codes_into_nospace (list[str], optional): Defaults to [].
        ignored_substrings_into_space (dict[str, list[str]], optional): Defaults to {}.
        ignored_substrings_into_nospace (dict[str, list[str]], optional): Defaults to {}.
        ignored_rules_languagetool (list[str], optional): Defaults to [].

    Returns:
        int: Id of the entry created
    """
    if not project_name:
        logger.error("project_name cannot be empty.")
        raise ValueError
    if not language:
        logger.error("Language cannot be empty.")
        raise ValueError

    data: dict[str, Item] = load_data()

    if project_name in data:
        logger.error("Project name already exists: %s", project_name)
        raise ValueError

    data[project_name] = {
        "language": language,
        "parser": parser,
        "specific_argument": specific_argument,
        "path_dictionary": path_dictionary,
        "valid_characters": valid_characters,
        "banwords": banwords or [],
        "ignored_codes_into_space": ignored_codes_into_space or [],
        "ignored_codes_into_nospace": ignored_codes_into_nospace or [],
        "ignored_substrings_into_space": ignored_substrings_into_space or {},
        "ignored_substrings_into_nospace": ignored_substrings_into_nospace or {},
        "ignored_rules_languagetool": ignored_rules_languagetool or [],
    }

    save_data(data)
    logger.info("Project '%s' created.", project_name)


def set_entry(
    project_name: str,
    language: str | None = None,
    parser: str | None = None,
    specific_argument: str | None = None,
    path_dictionary: str | None = None,
    valid_characters: str | None = None,
    banwords: list[str] | None = None,
    ignored_codes_into_space: list[str] | None = None,
    ignored_codes_into_nospace: list[str] | None = None,
    ignored_substrings_into_space: dict[str, list[str]] | None = None,
    ignored_substrings_into_nospace: dict[str, list[str]] | None = None,
    ignored_rules_languagetool: list[str] | None = None,
) -> None:
    """set the entry in the json, if arg not specified, it will not be changed
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        raise ValueError
    if language is not None:
        set_language(project_name, language)
    if parser is not None:
        set_parser(project_name, parser)
    if specific_argument is not None:
        set_specific_argument(project_name, specific_argument)
    if path_dictionary is not None:
        set_path_dictionary(project_name, path_dictionary)
    if valid_characters is not None:
        set_valid_characters(project_name, valid_characters)
    if banwords is not None:
        set_banwords(project_name, banwords)
    if ignored_codes_into_space is not None:
        set_ignored_codes_into_space(project_name, ignored_codes_into_space)
    if ignored_codes_into_nospace is not None:
        set_ignored_codes_into_nospace(project_name, ignored_codes_into_nospace)
    if ignored_substrings_into_space is not None:
        set_ignored_substrings_into_space(project_name, ignored_substrings_into_space)
    if ignored_substrings_into_nospace is not None:
        set_ignored_substrings_into_nospace(project_name, ignored_substrings_into_nospace)
    if ignored_rules_languagetool is not None:
        set_ignored_rules(project_name, ignored_rules_languagetool)
    logger.info("Entry %s updated.", project_name)
    return


def set_entry_from_item(project_name: str, data: Item) -> None:
    """set the entry in the json with a complete Item
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        raise ValueError
    if "language" not in data or data["language"] == "":
        logger.error("Language cannot be empty.")
        raise ValueError
    set_entry(
        project_name,
        language=data["language"],
        parser=data["parser"],
        specific_argument=data["specific_argument"],
        path_dictionary=data["path_dictionary"],
        valid_characters=data["valid_characters"],
        banwords=data["banwords"],
        ignored_codes_into_space=data["ignored_codes_into_space"],
        ignored_codes_into_nospace=data["ignored_codes_into_nospace"],
        ignored_substrings_into_space=data["ignored_substrings_into_space"],
        ignored_substrings_into_nospace=data["ignored_substrings_into_nospace"],
        ignored_rules_languagetool=data["ignored_rules_languagetool"]
    )


def delete_entry(project_name: str) -> None:
    """delete entry by id
    Args:
        project_name (str): id of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, Item] = load_data()
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
        raise ValueError
    if new_project_name == "":
        logger.error("project_name cannot be empty.")
        raise ValueError
    data: dict[str, Item] = load_data()
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
        raise ValueError
    if language == "":
        logger.error("Language cannot be empty.")
        raise ValueError
    data: dict[str, Item] = load_data()
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
        raise ValueError
    data: dict[str, Item] = load_data()
    data[project_name]["parser"] = parser
    save_data(data)


def set_specific_argument(project_name: str, specific_argument: str) -> None:
    """set the specific argument of the project

    Args:
        project_name (str): id of the project
        specific_argument (str): specific argument of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        raise ValueError
    data: dict[str, Item] = load_data()
    data[project_name]["specific_argument"] = specific_argument
    save_data(data)


def set_path_dictionary(project_name: str, path_dictionary: str) -> None:
    """set the path of the dictionary of the project

    Args:
        project_name (str): id of the project
        path_dictionary (str): path of the dictionary of the project
    """
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, Item] = load_data()
    data[project_name]["path_dictionary"] = path_dictionary
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
    data: dict[str, Item] = load_data()
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
    data: dict[str, Item] = load_data()
    for character in characters:
        if character not in data[project_name]["valid_characters"]:
            data[project_name]["valid_characters"] += character
    save_data(data)


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


def set_ignored_codes_into_nospace(project_name: str, codes: list[str]) -> None:
    """set the ignored codes into nospace of the project

    Args:
        project_name (str): id of the project
        codes (list[str]): codes to set
    """
    _set_to_list_field(project_name, "ignored_codes_into_nospace", codes)


def add_ignored_codes_into_nospace(project_name: str, code: str) -> None:
    """add a code to the ignored codes into nospace of the project
    Args:
        project_name (str): id of the project
        code (str): code to add
    """
    _add_to_list_field(project_name, "ignored_codes_into_nospace", code)


def remove_ignored_codes_into_nospace(project_name: str, code: str) -> None:
    """remove a code from the ignored codes into nospace of the project
    Args:
        project_name (str): id of the project
        code (str): code to remove
    """
    _remove_from_list_field(project_name, "ignored_codes_into_nospace", code)


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


def set_ignored_substrings_into_nospace(project_name: str, substrings: dict[str, list[str]]) -> None:
    """set the ignored substrings into nospace of the project

    Args:
        project_name (str): id of the project
        substrings (dict[str, list[str]]): substrings to set
    """
    _set_to_dict_list_field(project_name, "ignored_substrings_into_nospace", substrings)


def add_ignored_substrings_into_nospace(project_name: str, begin: str, end: str) -> None:
    """add a substring to the ignored substrings into nospace of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _add_to_dict_list_field(project_name, "ignored_substrings_into_nospace", begin, end)


def remove_ignored_substrings_into_nospace(project_name: str, begin: str, end: str) -> None:
    """remove a substring from the ignored substrings into nospace of the project
    Args:
        project_name (str): id of the project
        begin (str): beginning of the substring
        end (str): end of the substring
    """
    _remove_from_dict_list_field(project_name, "ignored_substrings_into_nospace", begin, end)


def set_ignored_rules(project_name: str, rules: list[str]) -> None:
    """set the ignored rules of the project

    Args:
        project_name (str): id of the project
        rules (list[str]): rules to set
    """
    _set_to_list_field(project_name, "ignored_rules_languagetool", rules)


def add_ignored_rules(project_name: str, rule: str) -> None:
    """add a rule to the ignored rules of the project
    Args:
        project_name (str): id of the project
        rule (str): rule to add
    """
    _add_to_list_field(project_name, "ignored_rules_languagetool", rule)


def remove_ignored_rules(project_name: str, rule: str) -> None:
    """remove a rule from the ignored rules of the project
    Args:
        project_name (str): id of the project
        rule (str): rule to remove
    """
    _remove_from_list_field(project_name, "ignored_rules_languagetool", rule)


# ------------------------------Internal utility functions---------------------

def _set_to_list_field(project_name: str, field: str, values: list[str]) -> None:
    """Set the field to a new list of values"""
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, Item] = load_data()
    data[project_name][field] = values
    save_data(data)


def _add_to_list_field(project_name: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, value):
        return
    data: dict[str, Item] = load_data()
    if value not in data[project_name][field]:
        data[project_name][field].append(value)  # type: ignore
        save_data(data)


def _remove_from_list_field(project_name: str, field: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, value):
        return
    data: dict[str, Item] = load_data()
    if value in data[project_name][field]:
        data[project_name][field].remove(value)  # type: ignore
        save_data(data)


def _set_to_dict_list_field(project_name: str, field: str, values: dict[str, list[str]]) -> None:
    """Set the field to a new dictionary of lists"""
    if not is_project_name_exist(project_name):
        log_error_id_invalid(project_name)
        return
    data: dict[str, Item] = load_data()
    data[project_name][field] = values
    save_data(data)


def _add_to_dict_list_field(project_name: str, field: str, key: str, value: str) -> None:
    if _log_error_if_id_or_value_invalid(project_name, key, value):
        return
    data: dict[str, Item] = load_data()
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
    data: dict[str, Item] = load_data()
    if key in data[project_name][field]:
        if value in data[project_name][field][key]:
            data[project_name][field][key].remove(value)  # type: ignore
        if not data[project_name][field][key]:
            del data[project_name][field][key]
    save_data(data)
