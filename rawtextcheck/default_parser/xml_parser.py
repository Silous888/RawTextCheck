"""
File        : xml_parser.py
Author      : Silous
Created on  : 2025-08-21
Description : Parser for xml files.

This module provides a function to parse an xml file and return its non-empty lines.
This parser acts as a default parser for xml files.
"""

# == Imports ==================================================================

from logging import Logger
import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils

from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


# == Constants ================================================================

TAG_ARG = ParserArgument(name="tag", optional=False)
ATTR_ARG = ParserArgument(name="attr", optional=True)
ID_ATTR_ARG = ParserArgument(name="idAttr", optional=True)

LIST_ARGUMENTS: list[ParserArgument] = [TAG_ARG, ATTR_ARG, ID_ATTR_ARG]


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def build_line_map(filepath: str) -> dict[int, str]:
    """Build a mapping of line numbers to raw content (stripped).

    Args:
        filepath (str): Path to the XML file.
    """
    line_map: dict[int, str] = {}
    with open(filepath, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line_map[i] = saxutils.unescape(line.rstrip("\n"))
    return line_map


def parse_file(filepath: str, arguments: dict[str, str]) -> list[tuple[str, str]]:
    """Parse an XML file and return non-empty texts with a row identifier.

    Args:
        filepath (str): Path to the XML file.
        arguments (dict[str, str]): Parser arguments.
            keys:
                - "tag": The XML element tag to extract.
                - "attr": (optional) Attribute name to extract instead of element text.
                - "idAttr": (optional) Attribute name to use as row identifier.
                           Defaults to line number in the file.

    Returns:
        list[tuple[str, str]]: List of (row ID as string, text/attribute content).
    """
    try:
        tag: str = arguments[TAG_ARG.name]
        attr: str | None = arguments.get(ATTR_ARG.name)
        id_attr: str | None = arguments.get(ID_ATTR_ARG.name)
    except KeyError as e:
        logger.error("Missing required argument: %s", e)
        return []

    results: list[tuple[str, str]] = []
    try:
        line_map: dict[int, str] = build_line_map(filepath)

        tree: ET.ElementTree[ET.Element[str]] = ET.parse(filepath)
        root: ET.Element[str] = tree.getroot()

        for elem in root.iter(tag):
            if attr:
                value: str = elem.attrib.get(attr, "").strip()
            else:
                value = (elem.text or "").strip()

            if not value:
                continue

            if id_attr and id_attr in elem.attrib:
                row_id: str = elem.attrib[id_attr].strip()
            else:
                row_id = "?"
                for line_no, raw in line_map.items():
                    if f"<{tag}" in raw and value in raw:
                        row_id = str(line_no)
                        break

            results.append((row_id, value))

        return results

    except Exception as e:
        logger.error("Error when parsing the XML file %s : %s", filepath, e)
        return []
