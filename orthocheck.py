from pathlib import Path
import csv
from io import StringIO

CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àâäāéèêëēîïôöùûüÿçœæáȧāãčęīłṇñóøōõšṣṭúūžẓ"
    "ÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇŒÆÁȦĀÃČĘĪŁṆÑÓØŌÕŠṢṬÚŽẒ-"
)


def parse_csv(csv_file: str) -> set[str]:
    words: set[str] = set()
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            words.add(row[0].lower())
    return words


def load_words(specific_csv: str | None = None) -> set[str]:
    words: set[str] = set()
    for path in Path('words').iterdir():
        if 'specific' in path.name and specific_csv is not None:
            if specific_csv in path.name:
                words = words.union(parse_csv(str(path)))
        elif path.name.endswith('.csv'):
            words = words.union(parse_csv(str(path)))
    return words


def check_string(string: str, existing_words: set[str], tags: dict[str, str] = {}) -> list[str]:
    f = StringIO(string)
    output: list[str] = []
    char: str = f.read(1)
    current_word: str = ""
    while True:
        if char in tags:
            read_until_occurrence(f, tags[char])
        elif char in CHARS and char != "":
            current_word += char

        else:
            if current_word != "":

                word_to_check = current_word.lower()

                if "-" in word_to_check:
                    if word_to_check not in existing_words:
                        for sub_word in word_to_check.split('-'):
                            if sub_word not in existing_words:
                                output.append(word_to_check)
                                break
                else:
                    if word_to_check not in existing_words:
                        output.append(current_word)

                current_word = ""

        if char == "":
            break
        char = f.read(1)

    return output


def check_file(path: str, encoding: str = 'utf-8', tags: dict[str, str] = {}) -> dict[int, list[str]]:
    existing_words: set[str] = load_words()
    output: dict[int, list[str]] = {}
    lines: list[str] = open(path, mode='r', encoding=encoding).readlines()
    for idx, line in enumerate(lines):
        mistake: list[str] = check_string(line, existing_words=existing_words, tags=tags)
        if len(mistake) != 0:
            output[idx + 1] = mistake
    return output


def read_until_occurrence(f: StringIO, end_char: str) -> None:
    char: str = f.read(1)
    while char not in [end_char, ""]:
        char = f.read(1)
