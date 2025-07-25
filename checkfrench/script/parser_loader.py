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
import importlib.util

from checkfrench.default_parameters import PLUGIN_PARSER_DIRECTORY, PARSERFUNCTIONTYPE
from checkfrench.logger import get_logger


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)


# == Functions ================================================================

def get_all_parsers() -> dict[str, PARSERFUNCTIONTYPE]:
    """
    Dynamically load all .py plugin files from a given directory,
    and extract their 'parse_file' function.

    Returns:
        dict[str, ParserFunction]: A mapping of module names to their parse_file functions.
    """
    parsers: dict[str, PARSERFUNCTIONTYPE] = {}

    os.makedirs(PLUGIN_PARSER_DIRECTORY, exist_ok=True)

    # Iterate over all .py files in the plugin directory
    for filename in os.listdir(PLUGIN_PARSER_DIRECTORY):
        if filename.endswith(".py"):
            module_name: str = filename[:-3]  # remove .py extension
            filepath: str = os.path.join(PLUGIN_PARSER_DIRECTORY, filename)

            # Load the module from the given file path
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    # Execute the module to load its contents
                    spec.loader.exec_module(module)

                    # Check if the module has a 'parse_file' function
                    if hasattr(module, "parse_file"):
                        # Store the parse_file function under the module's name
                        parsers[module_name] = getattr(module, "parse_file")

                except Exception as e:
                    logger.error("Error loading parser %s: %s", module_name, e)

    return parsers
