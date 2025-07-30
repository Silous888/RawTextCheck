"""
Package     : default_parser
Author      : Silous
Created on  : 2025-07-14
Description : Default parsers for various file types.
"""


# == Imports ==================================================================

from . import (
    csv_parser,
    excel_parser,
    google_sheet_parser,
    textfile_parser
)

from rawtextcheck.default_parameters import PARSERFUNCTIONTYPE


# == Constants ================================================================

LIST_DEFAULT_PARSER: dict[str, PARSERFUNCTIONTYPE] = {
    "csv": csv_parser.parse_file,
    "excel": excel_parser.parse_file,
    "textfile": textfile_parser.parse_file,
    "google sheet": google_sheet_parser.parse_file
}
"""Every default parsers provided by the application"""
