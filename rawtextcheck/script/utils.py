"""
File        : utils.py
Author      : Silous
Created on  : 2025-04-18
Description : Utility functions for various operations in the application.
"""


# == Imports ==================================================================

import csv
import re


# == Functions ================================================================

def sanitize_folder_name(name: str) -> str:
    """Sanitize a folder name by removing or replacing invalid characters.

    Args:
        name (str): The folder name to sanitize.

    Returns:
        str: The sanitized folder name.
    """
    # Replace forbidden characters with underscore
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove ASCII control characters
    name = ''.join(c for c in name if ord(c) >= 32)
    # Trim whitespace from the beginning and end
    name = name.strip()
    # Limit length to a safe maximum (255 characters)
    return name[:255]


def parse_attributes(line: str) -> dict[str, str]:
    """
    Parse key='value' or key="value" pairs from a string and return them as a dictionary.

    Args:
        line (str): The input string containing key="value" or key='value' pairs.

    Returns:
        dict[str, str]: Dictionary of parsed attributes.
    """
    pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')'
    matches: list[str] = re.findall(pattern, line)
    return {
        key: (val1 if val1 else val2)
        for key, val1, val2 in matches
        if (val1 if val1 else val2)  # only keep non-empty values
    }

def parse_suggestions(suggestions: str) -> list[str]:
    """Parse a suggestion string, respecting quoted commas."""

    def strip_surrounding_quotes(s: str) -> str:
        """Remove surrounding quotes only if the string starts and ends with the same quote."""
        if (s.startswith("'") and s.endswith("'")) or \
           (s.startswith('"') and s.endswith('"')):
            return s[1:-1]
        return s

    cleaned: list[str] = []
    try:
        reader = csv.reader(
            [suggestions.strip("[]")],
            skipinitialspace=True,
            quotechar="'",
            doublequote=False,
            escapechar=None
        )
        for row in reader:
            for s in row:
                s = strip_surrounding_quotes(s.strip())
                if s:
                    cleaned.append(s)
    except Exception:
        pass

    return cleaned