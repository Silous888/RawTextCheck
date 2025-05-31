from typing import TypedDict


class Item(TypedDict):

    # project_name: str as key
    language: str
    parser: str
    specific_argument: str
    path_dictionary: str
    valid_characters: str
    banwords: list[str]
    ignored_codes_into_space: list[str]
    ignored_codes_into_nospace: list[str]
    ignored_substrings_into_space: dict[str, list[str]]
    ignored_substrings_into_nospace: dict[str, list[str]]
    ignored_rules_languagetool: list[str]


class ItemResult(TypedDict):
    """Class to define the structure of the result item"""

    # id_error: str as key
    line_number: str
    line: str
    error: str
    error_type: str
    explanation: str
