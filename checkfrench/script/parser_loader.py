import os
import importlib.util
from typing import Callable

from checkfrench.default_parameters import PLUGIN_PARSER_DIRECTORY
# Define a type alias for a parser function: it takes (pathfile, argument) and returns a list of (str, str) tuples
ParserFunction = Callable[[str, str], list[tuple[str, str]]]


def get_all_parsers() -> dict[str, ParserFunction]:
    """
    Dynamically load all .py plugin files from a given directory,
    and extract their 'parse_file' function.

    Returns:
        dict[str, ParserFunction]: A mapping of module names to their parse_file functions.
    """
    parsers: dict[str, ParserFunction] = {}

    os.makedirs(PLUGIN_PARSER_DIRECTORY, exist_ok=True)

    # Iterate over all .py files in the plugin directory
    for filename in os.listdir(PLUGIN_PARSER_DIRECTORY):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # remove .py extension
            filepath = os.path.join(PLUGIN_PARSER_DIRECTORY, filename)

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
                    # If any error occurs while loading the module, print it
                    print(f"[Plugin Load Error] {module_name}: {e}")

    return parsers
