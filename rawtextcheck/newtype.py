"""
File        : newtype.py
Author      : Silous
Created on  : 2025-05-31
Description : Module defining new types for the application.

This module contains type definitions used throughout the application to ensure type safety and clarity.
It includes definitions for project items and result items,
which are used to structure data related to projects and results of language checks.
"""


# == Imports ==================================================================

from typing import TypedDict


# == Classes ==================================================================

class ItemProject(TypedDict):
    """TypedDict for project items.
    This class defines the structure of a project item, including its attributes.
    Attributes:
        language (str): The language code for the project.
        parser (str): The parser used for the project.
        arg_parser (str): The argument parser for the project.
        valid_characters (str): Valid characters for the project.
        dictionary (list[str]): List of words in the project's dictionary.
        banwords (list[str]): List of words to ban in the project.
        ignored_codes_into_space (list[str]): List of codes to ignore, replacing with space.
        ignored_codes_into_nothing (list[str]): List of codes to ignore, replacing with nothing.
        ignored_substrings_into_space (dict[str, list[str]]): Substrings to ignore, replacing with space.
        ignored_substrings_into_nothing (dict[str, list[str]]): Substrings to ignore, replacing with nothing.
        ignored_rules (list[str]): List of LanguageTool rules to ignore.
    """

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


class ItemResult(TypedDict):
    """TypedDict for result items.
    This class defines the structure of a result item, including its attributes.
    Attributes:
        line_number (str): The line number where the error occurs.
        line (str): The text of the line where the error occurs.
        error (str): Description of the error.
        error_type (str): Type of the error.
        error_issue_type: category of the error, used to find spelling error
        explanation (str): Explanation of the error.
        suggestion (str): Suggested correction for the error.
    """
    # id_error: str as key
    line_number: str
    line: str
    error: str
    error_type: str
    error_issue_type: str
    explanation: str
    suggestion: str


class ItemConfig(TypedDict):
    """TypedDict for config file
    This class defines the structure of the config file
    Attributes:
        language (str): language of the app interface
        theme (str): theme for the apparence
        hidden_column (list[str]): last config for visibility of column of result table
        last_project (str): name of the last project, to reload it at launch
        """
    language: str
    theme: str
    hidden_column: list[str]
    last_project: str
    credentials_google: dict[str, str]
