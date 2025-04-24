from datetime import datetime
import json
import os
from typing import Any
from script import json_projects, utils


data_json: dict[str, Any] = {}


def save_result_process_one_str(id_game: int, name_file: str, method: int, data: list[tuple[int, str]]) -> None:
    folder_name: str = json_projects.data_json_projects[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def save_result_process_two_str(id_game: int, name_file: str, method: int, data: list[tuple[int, str, str]]) -> None:
    folder_name: str = json_projects.data_json_projects[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_result_process(id_game: int, name_file: str) -> tuple[list[Any], list[str]]:
    result: list[list[Any]] = [[], [], []]
    modification_dates: list[str] = []
    folder_name: str = json_projects.data_json_projects[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name, name_file + ".json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            result = json.load(file)
        modification_time: float = os.path.getmtime(path)
        modification_date: str = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M')
        modification_dates.append(modification_date)
    else:
        modification_dates.append("jamais lancée")
    return result, modification_dates


def remove_entry(id_game: int, name_file: str, method: int, value: str, text: str) -> None:

    print(id, name_file, method, value, text)
    folder_name: str = json_projects.data_json_projects[id_game]["folder_name"]  # type: ignore
    path: str = os.path.join("result", folder_name)
    with open(os.path.join(path, name_file + ".json"), "r", encoding="utf-8") as file:
        data = json.load(file)

    value_int: int | None = utils.safe_str_to_int(value)
    if value_int is None:
        return
    data: list[str] = [entry for entry in data if entry[:2] != [value_int, text]]  # type: ignore

    with open(os.path.join(path, name_file + ".json"), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
