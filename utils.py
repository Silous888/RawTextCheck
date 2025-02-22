import re


def extract_google_drive_id(url_or_id: str) -> str:
    """Extract the Google Drive ID (Sheets, Folders, or Files) from a given URL or return the ID if already valid.

    Args:
        url_or_id (str): The Google Drive URL or ID.

    Returns:
        str: The extracted ID, or an empty string if no match is found.
    """
    if re.match(r"^[a-zA-Z0-9-_]+$", url_or_id):
        return url_or_id

    match: re.Match[str] | None = re.search(r"/(?:d|folders)/([a-zA-Z0-9-_]+)", url_or_id)
    return match.group(1) if match else ""


def get_position_letter_alphabet(letter: str) -> int:
    """get the letter of the alphabet given a position

    Args:
        letter (str): letter of the alphabet

    Returns:
        int: position of the letter in the alphabet
    """
    return ord(letter.upper()) - ord("A") + 1


def safe_str_to_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def extract_before_arrow(text: str) -> str:
    match: re.Match[str] | None = re.match(r"^(.*?)\s*=>", text)
    return match.group(1) if match else ""
