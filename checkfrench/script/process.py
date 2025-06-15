""""main process of the application"""

# -------------------- Import Lib Standard -------------------
import re

# -------------------- Import Lib User -------------------
from checkfrench.api import google_drive_api as gdrive
from checkfrench.script import languagetool as languagetool
from checkfrench.script import utils


list_sentences_current_sheet: list[str] = []


def get_name_and_type_of_url(url: str) -> tuple[str, str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: dict[str, str] | int = gdrive.get_file_metadata(utils.extract_google_drive_id(url))
        if not isinstance(output, int):
            return output["name"], output["mimeType"]
    except Exception:
        return -1
    return -2


def get_sheet_name_in_folder(url_folder: str) -> list[str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: list[list[str]] | int = gdrive.list_spreadsheet_in_folder(utils.extract_google_drive_id(url_folder))
        if not isinstance(output, int):
            return [item[0] for item in output]
    except Exception:
        return -1
    return -2


def get_sheet_url_in_folder(url_folder: str) -> list[str] | int:
    """call get_file_metadata of google_drive_api and return name and mimeType of the file
    Args:
        url (str): url of the file

    Returns:
        tuple[str, str] | int : name and mimeType of the file, error code otherwise
    """
    try:
        output: list[list[str]] | int = gdrive.list_spreadsheet_in_folder(utils.extract_google_drive_id(url_folder))
        if not isinstance(output, int):
            return [item[1] for item in output]
    except Exception:
        return -1
    return -2


def remove_ignored_substrings(text: str, ignored_substrings: dict[str, str], insert_space: bool) -> str:
    """Remove substrings from text that are enclosed by any of the ignored substrings.

    Args:
        text (str): The input text.
        ignored_substrings (dict[str, str]): A dictionary where keys are the starting
        substrings and values are the ending substrings.
        insert_space (bool): Whether to insert a space where substrings are removed.

    Returns:
        str: The text with the ignored substrings removed.
    """
    for start, end in ignored_substrings.items():
        pattern: str = re.escape(start) + r'.*?' + re.escape(end)
        replacement: str = ' ' if insert_space else ''
        text = re.sub(pattern, replacement, text)  # Remove all matches of the pattern
    return text


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


def language_tool_initialize() -> None:
    """call initialize_tool of languagetool
    """
    languagetool.initialize_tool()


def language_tool_close() -> None:
    """call close_tool of languagetool
    """
    languagetool.close_tool()
