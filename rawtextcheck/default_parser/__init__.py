"""
Package     : default_parser
Author      : Silous
Created on  : 2025-07-14
Description : Default parsers for various file types.
"""


# == Imports ==================================================================

from types import ModuleType

from . import (
    csv_parser,
    excel_parser,
    po_parser,
    google_sheet_parser,
    textfile_parser,
    xml_parser
)


# == Constants ================================================================

LIST_DEFAULT_PARSER: dict[str, ModuleType] = {
    "csv": csv_parser,
    "excel": excel_parser,
    "google sheet": google_sheet_parser,
    "pofile": po_parser,
    "textfile": textfile_parser,
    "xml": xml_parser
}
"""Every default parsers provided by the application"""
