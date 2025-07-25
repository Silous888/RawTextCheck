"""
Package     : default_parser
Author      : Silous
Created on  : 2025-07-14
Description : Default parsers for various file types.
"""


# == Imports ==================================================================

from typing import Callable

from . import textfile_parser, excel_parser, csv_parser


# == Constants ================================================================

LIST_DEFAULT_PARSER: dict[str, Callable[[str, str], list[tuple[str, str]]]] = {
    "textfile": textfile_parser.parse_file,
    "excel": excel_parser.parse_file,
    "csv": csv_parser.parse_file
}
"""Every default parsers provided by the application"""
