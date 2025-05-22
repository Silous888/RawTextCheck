import json
import os
from typing import TypedDict


from checkfrench.script.utils import sanitize_folder_name
from default_parameters import RESULTS_FOLDER_PATH


"""
structure of the files:
in the results folder
    - name of the project (folder)
        - name of the file with the extension of the original file (json file)
"""


class ItemResult(TypedDict):
    """Class to define the structure of the result item"""

    # id_error: str as key
    line_number: int
    line: str
    error: str
    error_type: str
    explanation: str


def save_data(title_project: str, name_file: str, data: dict[str, ItemResult]) -> None:
    """save the data in a result json file

    Args:
        title_project (int): id of the project
        name_file (str): name of the file
        data (dict[str, Any]): data to save
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    file_path: str = os.path.join(folder_path, name_file)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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
        data[id_error] = item

    return data


def get_file_data(title_project: str, name_file: str) -> dict[str, ItemResult]:
    """get the data from a result json file

    Args:
        title_project (int): id of the project
        name_file (str): name of the file

    Returns:
        dict[str, Any]: data from the file
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    file_path: str = os.path.join(folder_path, name_file)

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    return data


def get_folder_data(title_project: str) -> list[tuple[str, dict[str, ItemResult]]]:
    """get the data from a result json file

    Args:
        title_project (int): id of the project

    Returns:
        list[str, dict[str, ItemResult]]: list of files and their data
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    files: list[str] = os.listdir(folder_path)

    data: list[tuple[str, dict[str, ItemResult]]] = []
    for file in files:
        file_path: str = os.path.join(folder_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            data.append((file, json.load(f)))

    return data


def delete_entry(title_project: str, name_file: str, id_error: str) -> None:
    """delete an entry in a result json file

    Args:
        title_project (int): id of the project
        name_file (str): name of the file
        id_error (str): id of the error to delete
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    file_path: str = os.path.join(folder_path, name_file)

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    if id_error in data:
        del data[id_error]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def delete_error_type(title_project: str, name_file: str, error_type: str) -> None:
    """delete all errors of a specific type in a result json file

    Args:
        title_project (int): id of the project
        name_file (str): name of the file
        error_type (str): type of the error to delete
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    file_path: str = os.path.join(folder_path, name_file)

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    data = {k: v for k, v in data.items() if v["error_type"] != error_type}

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def delete_specific_error_with_type(title_project: str, name_file: str, error_type: str, error: str) -> None:
    """delete all errors of a specific type and error in a result json file

    Args:
        title_project (int): id of the project
        name_file (str): name of the file
        error_type (str): type of the error to delete
        error (str): error to delete
    """
    folder_path: str = os.path.join(RESULTS_FOLDER_PATH,
                                    sanitize_folder_name(title_project))
    file_path: str = os.path.join(folder_path, name_file)

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data: dict[str, ItemResult] = json.load(f)

    data = {k: v for k, v in data.items() if v["error_type"] != error_type or v["error"] != error}

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
