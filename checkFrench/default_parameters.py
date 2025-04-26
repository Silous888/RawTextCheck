
from pathlib import Path


JSON_FILE_PATH: Path = Path(__file__).parent / "json_data_projects.json"


DEFAULT_VALID_LETTERS: str = "0123456789" \
                             "abcdefghijklmnopqrstuvwxyz" \
                             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DEFAULT_VALID_PUNCTUATION: str = ".,;:!?" \
                                 "()[]<>\"'" \
                                 "-+=" \
                                 " "  # Space
