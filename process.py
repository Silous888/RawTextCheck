""""main process of the application"""

import json
from typing import Any

data: dict[str, Any] = {}


def load_json() -> dict[str, Any]:
    """load json data
    """
    with open("./json_data_jeux.json", "r", encoding="utf-8") as file:
        return json.load(file)
