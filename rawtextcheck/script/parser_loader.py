"""
Package     : parser_loader
Author      : Silous
Created on  : 2025-07-25
Description : Dynamically load parsers from a specified directory.

This module provides functionality to dynamically load parser functions
from Python files located in a specified directory. It is useful for
extending the application with custom parsers without modifying the core code.
"""


# == Imports ==================================================================

import os
from logging import Logger
from importlib.machinery import ModuleSpec
import importlib.util
from types import ModuleType

from rawtextcheck.default_parameters import PLUGIN_PARSER_FOLDER
from rawtextcheck.default_parser import LIST_DEFAULT_PARSER
from rawtextcheck.logger import get_logger
from rawtextcheck.newtype import ParserArgument


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def get_all_parsers() -> dict[str, ModuleType]:
    """
    Dynamically load all .py plugin files from a given directory,
    and extract their 'parse_file' function.

    Returns:
        dict[str, ParserFunction]: A mapping of module names to their parse_file functions.
    """
    plugin_parser: dict[str, ModuleType] = {}

    os.makedirs(PLUGIN_PARSER_FOLDER, exist_ok=True)

    # Iterate over all .py files in the plugin directory
    for filename in os.listdir(PLUGIN_PARSER_FOLDER):
        if filename.endswith(".py"):
            module_name: str = filename[:-3]  # remove .py extension
            filepath: str = os.path.join(PLUGIN_PARSER_FOLDER, filename)

            # Load the module from the given file path
            spec: ModuleSpec | None = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module: ModuleType = importlib.util.module_from_spec(spec)
                try:
                    # Execute the module to load its contents
                    spec.loader.exec_module(module)

                    # Check if the module has a 'parse_file' function
                    if hasattr(module, "parse_file"):
                        # Store the parse_file function under the module's name
                        plugin_parser[module_name] = module
                except Exception as e:
                    logger.error("Error loading parser %s: %s", module_name, e)

    all_parsers: dict[str, ModuleType] = {
        **LIST_DEFAULT_PARSER,
        **plugin_parser
    }
    return all_parsers


def call_is_filepath_valid(parser_name: str, filepath: str) -> tuple[bool, bool]:
    """call is_filepath_valid of a parser, and return result and existence of the
    method in the parser

    Args:
        parser_name (str): name of the parser
        filepath (str): filepath to test

    Returns:
        tuple[bool, bool]: is_filepath_valid result, if is_filepath_valid exists
    """
    all_parsers: dict[str, ModuleType] = get_all_parsers()
    if parser_name not in all_parsers:
        return False, False
    if hasattr(all_parsers[parser_name], "is_filepath_valid"):
        try:
            return all_parsers[parser_name].is_filepath_valid(filepath), True
        except Exception as e:
            logger.error("error during is_filepath_valid method of parser %s: %s", parser_name, e)
            return False, True
    else:
        return False, False


def call_get_filename(parser_name: str, filepath: str) -> tuple[str, bool]:
    """call get_filename of a parser, and return result, and existence of
    the method in the parser

    Args:
        parser_name (str): name of the parser
        filepath (str): filepath of the file

    Returns:
        tuple[str, bool]: result of get_filename, and if get_filename exists
    """
    all_parsers: dict[str, ModuleType] = get_all_parsers()
    if parser_name not in all_parsers:
        return "", False
    if hasattr(all_parsers[parser_name], "get_filename"):
        try:
            return all_parsers[parser_name].get_filename(filepath), True
        except Exception as e:
            logger.error("error during get_filename method of parser %s: %s", parser_name, e)
            return "", True
    else:
        return "", False


def get_arguments_keys(parser_name: str) -> tuple(list[ParserArgument], bool):  # type: ignore
    """call LIST_ARGUMENT of the parser, and return the list, and existence
    of the list in the parser.

    Args:
        parser_name (str): name of the parser

    Returns:
        tuple[list[str], bool]: list of the argument keys, and existence of LIST_ARGUMENT
    """
    all_parsers: dict[str, ModuleType] = get_all_parsers()
    if parser_name not in all_parsers:
        return ParserArgument(name="", optional=True), False
    if hasattr(all_parsers[parser_name], "LIST_ARGUMENTS"):
        return all_parsers[parser_name].LIST_ARGUMENTS, True
    else:
        return ParserArgument(name="", optional=True), False
