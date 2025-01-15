import re


def extract_google_sheet_id(url: str) -> str:
    """Extract the Google Sheets ID from a given URL.

    Args:
        url (str): The Google Sheets URL.

    Returns:
        str: The extracted ID, or an empty string if no match is found.
    """
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
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
    return ord(letter.upper()) - ord("A")
