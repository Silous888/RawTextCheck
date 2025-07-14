"""
File        : json_results.py
Author      : Silous
Created on  : 2025-04-24
Description : Module for managing results of language check, stored JSON files.

This module provides functions to load, save, and manipulate JSON files that contain results of language checks.
The results are stored in a specific folder structure, where each project has its own folder,
and each file within that project has its own JSON file.
The JSON files contain a dictionary of results, where each key is a unique identifier for an error,
and the value is a dictionary containing details about the error.

The JSON structure is expected to follow the `ItemResult` TypedDict definition.

Features:
- Saving data
- Loading data
- Generating unique error IDs
- Deleting specific entries

Dependencies:
- checkfrench.default_parameters.RESULTS_FOLDER_PAH: path to the JSON results folder
- checkfrench.script.utils.sanitize_folder_name: used for result folder naming
- checkfrench.newtype.ItemResult: type definition for result items
"""


# == Imports ==================================================================

import json
from logging import Logger
import os

from checkfrench.default_parameters import RESULTS_FOLDER_PATH
from checkfrench.logger import get_logger
from checkfrench.newtype import ItemResult
from checkfrench.script.utils import sanitize_folder_name


# == Global Variables =========================================================

logger: Logger = get_logger(__name__)
JSON_EXT: str = ".json"


# == Functions ================================================================

def save_data(project_name: str, filename: str, data: dict[str, ItemResult]) -> None:
    """save the data in a result json file

    Args:
        project_name (str): id of the project
        filename (str): name of the file
        data (dict[str, ItemResult]): data to save
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, os.path.basename(filename) + JSON_EXT)

    # Create the folder if it doesn't exist
    os.makedirs(folderpath, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Result of %s from project %s saved.", filename, project_name)


def generate_id_errors(result: list[ItemResult]) -> dict[str, ItemResult]:
    """generate the id of the errors
    ex: 1a, 1b, 2a, 3a, 3b, 3c, 3d
    where 1, 2, 3 are the line numbers and
    a, b, c, d are the letters incremented for unique id

    Args:
        result (list[ItemResult]): list of errors

    Returns:
        dict[str, ItemResult]: dictionary with the id as key
    """
    data: dict[str, ItemResult] = {}

    for item in result:
        id_error: str = f"{item['line_number']}a"
        if id_error in data:
            # if the id already exists, increment the letter
            i: int = 1
            while id_error in data:
                id_error = f"{item['line_number']}{chr(97 + i)}"
                i = i + 1
        data[id_error] = item

    return data


def is_result_exists(project_name: str, filename: str) -> bool:
    """Test if a result file exists

    Args:
        project_name (str): id of the project
        filename (str): name of the file

    Returns:
        bool: True if the file exists, False otherwise
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, filename + JSON_EXT)

    return os.path.isfile(filepath)


def get_file_data(project_name: str, filename: str) -> dict[str, ItemResult]:
    """get the data from a result json file

    Args:
        project_name (str): id of the project
        filename (str): name of the file

    Returns:
        dict[str, ItemResult]: data from the file
    """
    if not is_result_exists(project_name, filename):
        logger.warning("Result for file %s does not exist in project %s.", filename, project_name)
        return {}

    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, filename + JSON_EXT)

    with open(filepath, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    logger.info("Read result of %s from project %s.", filename, project_name)

    return data


def get_folder_data(project_name: str) -> list[tuple[str, dict[str, ItemResult]]]:
    """get the data from every results of a project

    Args:
        project_name (str): id of the project

    Returns:
        list[str, dict[str, ItemResult]]: list of files and their data
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    files: list[str] = os.listdir(folderpath)

    data: list[tuple[str, dict[str, ItemResult]]] = []
    for file in files:
        data.append((file, get_file_data(project_name, file)))

    return data


def delete_entry(project_name: str, filename: str, id_error: str) -> int:
    """delete an entry in a result json file

    Args:
        project_name (str): id of the project
        filename (str): name of the file
        id_error (str): id of the error to delete

    Returns:
        int: 0 if success, 1 if file does not exist, 2 if error not found
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, filename + JSON_EXT)

    if not os.path.exists(filepath):
        logger.warning("Result for file %s does not exist in project %s.", filename, project_name)
        return 1

    with open(filepath, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    if id_error in data:
        del data[id_error]
    else:
        logger.warning("Error %s not found in %s.", id_error, filename)
        return 2

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info("Deleted error %s from %s.", id_error, filename)
    return 0


def delete_error_type(project_name: str, filename: str, error_type: str) -> None:
    """delete all errors of a specific type in a result json file

    Args:
        project_name (str): id of the project
        filename (str): name of the file
        error_type (str): type of the error to delete
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, filename + JSON_EXT)

    if not os.path.exists(filepath):
        logger.warning("Result for file %s does not exist in project %s.", filename, project_name)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    data = {k: v for k, v in data.items() if v["error_type"] != error_type}

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info("Deleted error type %s from %s.", error_type, filename)


def delete_specific_error_with_type(project_name: str, filename: str, error_type: str, error: str) -> None:
    """delete all errors of a specific type and error in a result json file

    Args:
        project_name (str): id of the project
        filename (str): name of the file
        error_type (str): type of the error to delete
        error (str): error to delete
    """
    folderpath: str = os.path.join(RESULTS_FOLDER_PATH,
                                   sanitize_folder_name(project_name))
    filepath: str = os.path.join(folderpath, filename + JSON_EXT)

    if not os.path.exists(filepath):
        logger.warning("Result for file %s does not exist in project %s.", filename, project_name)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    data = {k: v for k, v in data.items() if v["error_type"] != error_type or v["error"] != error}

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info("Deleted error %s of type %s from %s.", error, error_type, filename)
