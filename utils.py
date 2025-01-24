import re
from io import StringIO


def extract_google_sheet_id(url_or_id: str) -> str:
    """Extract the Google Sheets ID from a given URL.

    Args:
        url (str): The Google Sheets URL.

    Returns:
        str: The extracted ID, or an empty string if no match is found.
    """
    if re.match(r"^[a-zA-Z0-9-_]+$", url_or_id):
        return url_or_id
    match: re.Match[str] | None = re.search(r"/d/([a-zA-Z0-9-_]+)", url_or_id)
    if match:
        return match.group(1)
    return ""


def get_position_letter_alphabet(letter: str) -> int:
    """get the letter of the alphabet given a position

    Args:
        letter (str): letter of the alphabet

    Returns:
        int: position of the letter in the alphabet
    """
    return ord(letter.upper()) - ord("A") + 1


def read_until_occurrence(f: str, end_char: str) -> None:
    fs = StringIO(f)
    char: str = fs.read(1)
    while char not in [end_char, ""]:
        char = fs.read(1)
