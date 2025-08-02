"""
File        : process.py
Author      : Silous
Created on  : 2025-04-18
Description : functions to analyse a file and generate errors.

This module provides functions to process a file, analyze its content,
and generate errors based on specific criteria such as invalid characters,
banwords, and ignored substrings. It integrates with a parser and a language
tool to perform the analysis and returns structured results.
"""

# == Imports ==================================================================

from logging import Logger
import os
from types import ModuleType

from rawtextcheck import default_parser
from rawtextcheck.default_parameters import (
    INVALID_CHAR_TEXT_ERROR_TYPE,
    INVALID_CHAR_TEXT_ERROR,
    BANWORD_TEXT_ERROR_TYPE,
    BANWORD_TEXT_ERROR
    )

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ItemProject, ItemResult
from rawtextcheck.script import json_projects, json_results, languagetool, parser_loader, utils


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def remove_ignored_substrings(text: str, ignored_substrings: dict[str, list[str]], insert_space: bool) -> str:
    """Remove substrings from text that are enclosed by any of the ignored substrings.

    Args:
        text (str): The input text.
        ignored_substrings (dict[str, list[str]]): A dictionary where keys are the starting
        substrings and values are lists of possible ending substrings.
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        str: The text with the ignored substrings removed.
    """
    i: int = 0
    result: list[str] = []  # Accumulator for the final result
    length: int = len(text)

    # Loop through the text character by character
    while i < length:
        matched = False  # Flag to know if a substring was matched and skipped

        for start, ends in ignored_substrings.items():

            if text.startswith(start, i):
                start_index: int = i + len(start)
                end_index: int = length  # Default to end of string if no end is found
                found = False  # Flag to signal a successful end match

                # Look for the first matching end pattern after the start
                for j in range(start_index, length):
                    for end in ends:
                        # If the text at position j starts with an end pattern
                        if text.startswith(end, j):
                            end_index = j + len(end)  # Define where the ignored block ends
                            found = True
                            break
                    if found:
                        break

                if found:
                    if insert_space:
                        result.append(' ')
                    i = end_index  # Move index to the end of the ignored block
                    matched = True  # Mark the match
                    break

        # If no start pattern matched at current position, keep the character
        if not matched:
            result.append(text[i])  # Append current character to result
            i += 1

    # Join all parts into a single string and return
    return ''.join(result)


def remove_ignored_codes(text: str, ignored_codes: list[str], insert_space: bool) -> str:
    """Remove codes of the game from the string

    Args:
        text (str): The input text.
        ignored_codes (dict[str]): A dictionary where codes to removes
        substrings and values are the ending substrings.
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        str: The text with the ignored substrings removed.
    """
    for code in ignored_codes:
        if insert_space:
            text = text.replace(code, " ")
        else:
            text = text.replace(code, "")
    return text


def remove_ignored_elements_in_texts(
        texts: list[tuple[str, str]],
        ignored_codes_into_space: list[str], ignored_codes_into_nothing: list[str],
        ignored_substrings_into_space: dict[str, list[str]], ignored_substrings_into_nothing: dict[str, list[str]]
        ) -> list[tuple[str, str]]:
    """call remove_ignored_substrings and remove_ignored_codes on every line
    ignored codes will be processed first, then ignored substrings

    Args:
        texts (list[tuple[str, str]]): list of every [line number, line text]
        ignored_codes_into_space (list[str]): List of codes to ignore, replacing with space.
        ignored_codes_into_nothing (list[str]): List of codes to ignore, replacing with nothing.
        ignored_substrings_into_space (dict[str, list[str]]): Substrings to ignore, replacing with space.
        ignored_substrings_into_nothing (dict[str, list[str]]): Substrings to ignore, replacing with nothing.

    Returns:
        list[tuple[str, str]]: texts with ignored elements removed
    """
    cleaned_texts: list[tuple[str, str]] = []

    for line_number, line in texts:
        line = remove_ignored_codes(line, ignored_codes_into_space, insert_space=True)
        line = remove_ignored_codes(line, ignored_codes_into_nothing, insert_space=False)

        line: str = remove_ignored_substrings(line, ignored_substrings_into_space, insert_space=True)
        line = remove_ignored_substrings(line, ignored_substrings_into_nothing, insert_space=False)

        if line:
            cleaned_texts.append((line_number, line))

    return cleaned_texts


def generate_errors_invalid_characters(texts: list[tuple[str, str]], valid_characters: str) -> list[ItemResult]:
    """create errors for invalid characters in line of texts

    Args:
        texts (list[tuple[str, str]]): The input text
        valid_characters (str): valid characters of the text

    Returns:
        list[ItemResult]: invalid characters errors
    """
    invalid_characters_found: list[ItemResult] = []

    for line_number, line in texts:
        for c in line:
            if c not in valid_characters:
                invalid_characters_found.append(
                    ItemResult(line_number=line_number,
                               line=line,
                               error=c,
                               error_type=INVALID_CHAR_TEXT_ERROR_TYPE,
                               error_issue_type=INVALID_CHAR_TEXT_ERROR_TYPE,
                               explanation=INVALID_CHAR_TEXT_ERROR,
                               suggestion="")
                )
    return invalid_characters_found


def generate_errors_banwords(texts: list[tuple[str, str]], banwords: list[str]) -> list[ItemResult]:
    """create errors for banword in line of texts

    Args:
        texts (list[tuple[str, str]]): The input text
        banwords (list[str]): banwords of the text

    Returns:
        list[ItemResult]: banword errors
    """
    banwords_found_in_text: list[ItemResult] = []

    for line_number, line in texts:
        for word in line.split():
            if word in banwords:
                banwords_found_in_text.append(
                    ItemResult(line_number=line_number,
                               line=line,
                               error=word,
                               error_type=BANWORD_TEXT_ERROR_TYPE,
                               error_issue_type=BANWORD_TEXT_ERROR_TYPE,
                               explanation=BANWORD_TEXT_ERROR,
                               suggestion="")
                )
    return banwords_found_in_text


def process_file(filepath: str, project_name: str, argument_parser: str) -> None:
    """generate errors of a file

    Args:
        filepath (str): path of the file
        project_name (str): project_name, for how to manage process of the file
        argument_parser (str): argument for the parser
    """

    project_data: ItemProject | None = json_projects.get_project_data(project_name)
    if project_data is None:
        return

    # Merge default and dynamic parsers
    all_parsers: dict[str, ModuleType] = {
        **default_parser.LIST_DEFAULT_PARSER,
        **parser_loader.get_all_parsers()
    }

    parser_name: str = project_data["parser"]
    if parser_name not in all_parsers:
        return

    # Parse the file using the selected parser
    argument_parser_dict: dict[str, str] = utils.parse_attributes(argument_parser)
    texts: list[tuple[str, str]] = all_parsers[parser_name].parse_file(filepath, argument_parser_dict)

    texts = remove_ignored_elements_in_texts(
        texts,
        project_data["ignored_codes_into_space"],
        project_data["ignored_codes_into_nothing"],
        project_data["ignored_substrings_into_space"],
        project_data["ignored_substrings_into_nothing"]
    )

    languagetool.initialize_tool(project_data["language"])
    languagetool_result: list[ItemResult] = languagetool.analyze_text(texts,
                                                                      project_data["dictionary"],
                                                                      project_data["ignored_rules"])

    invalid_characters_result: list[ItemResult] = generate_errors_invalid_characters(
        texts,
        project_data["valid_characters"]
        )

    banwords_result: list[ItemResult] = generate_errors_banwords(texts, project_data["banwords"])

    line_order: dict[str, int] = {line_number: idx for idx, (line_number, _) in enumerate(texts)}

    all_result: list[ItemResult] = sorted(
        languagetool_result + invalid_characters_result + banwords_result,
        key=lambda item: (line_order.get(item["line_number"], float('inf')))
    )

    data: dict[str, ItemResult] = json_results.generate_id_errors(all_result)

    filename: str = filepath
    result, success = parser_loader.call_get_filename(parser_name, filepath)
    if success:
        filename = result
    else:
        filename = os.path.basename(filepath)

    json_results.save_data(project_name, filename, data)
