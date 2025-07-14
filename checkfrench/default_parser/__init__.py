"""
Package     : default_parser
Author      : Silous
Created on  : 2025-06-15
Description : Default parsers for various file types.
"""


# == Imports ==================================================================

import typing

from . import textfile_parser, excel_parser


# == Constants ================================================================

LIST_DEFAULT_PARSER: dict[str, typing.Callable[[str, str], list[tuple[str, str]]]] = {
    "textfile": textfile_parser.parse_file,
    "excel": excel_parser.parse_file
}
"""Every default parsers provided by the application"""
