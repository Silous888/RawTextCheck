""""main process of the application"""

import json
from typing import Any

data: dict[str, Any] = {}

ID_SHEET_DICT_GAME: str = "1tjUT3K4kX5_ArT6GXXovWEMf1JmeQRr6_JiqxBCSVrc"


def load_json() -> dict[str, Any]:
    """load json data
    """
    with open("./json_data_jeux.json", "r", encoding="utf-8") as file:
        return json.load(file)
