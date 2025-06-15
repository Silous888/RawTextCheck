from typing import TypedDict


class ItemProject(TypedDict):

    # project_name: str as key
    language: str
    parser: str
    arg_parser: str
    valid_characters: str
    dictionary: list[str]
    banwords: list[str]
    ignored_codes_into_space: list[str]
    ignored_codes_into_nothing: list[str]
    ignored_substrings_into_space: dict[str, list[str]]
    ignored_substrings_into_nothing: dict[str, list[str]]
    ignored_rules: list[str]
    synchronized_path: str


class ItemResult(TypedDict):
    """Class to define the structure of the result item"""

    # id_error: str as key
    line_number: str
    line: str
    error: str
    error_type: str
    explanation: str
    suggestion: str
