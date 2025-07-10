
"""
File        : textfile_parser.py
Author      : Silous
Created on  : 2025-06-15
Description : Parser for plain text files.

This module provides a function to parse a text file and return its non-empty lines.
This parser acts as a default parser for text files.
"""


def parse_file(pathfile: str, argument: str) -> list[tuple[str, str]]:
    """Parse a file and return each non-empty line with its line number.

    Args:
        pathfile (str): Path of the file.
        argument (str): Specific argument for this file (not used).

    Returns:
        list[tuple[str, str]]: List of tuples (line number as string, line content).
    """
    lines: list[tuple[str, str]] = []

    with open(pathfile, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            stripped: str = line.strip()
            if stripped:
                lines.append((str(i), stripped))

    return lines
