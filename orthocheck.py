from pathlib import Path
import csv
from io import StringIO

CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àâäāéèêëēîïôöùûüÿçœæáȧāãčęīłṇñóøōõšṣṭúūžẓ"
    "ÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇŒÆÁȦĀÃČĘĪŁṆÑÓØŌÕŠṢṬÚŽẒ-"
)

dictionay_words: set[str] = set()


def parse_csv(csv_file: str) -> set[str]:
    words: set[str] = set()
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            words.add(row[0].lower())
    return words


def load_words(folder_dict_name: str) -> set[str]:
    words: set[str] = set()
    for path in Path(folder_dict_name).iterdir():
        if path.name.endswith('.csv'):
            words = words.union(parse_csv(str(path)))
    return words


def check_string(string: str, existing_words: set[str]) -> list[str]:
    f = StringIO(string)
    output: list[str] = []
    char: str = f.read(1)
    current_word: str = ""
    while True:
        if char in CHARS and char != "":
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


def read_until_occurrence(f: StringIO, end_char: str) -> None:
    char: str = f.read(1)
    while char not in [end_char, ""]:
        char = f.read(1)


def process_orthocheck(list_sentences: list[str]) -> list[tuple[int, str]]:
    output_process: list[tuple[int, str]] = []
    for index, sentence in enumerate(list_sentences):
        output_ortho: list[str] = check_string(sentence, dictionay_words)
        if output_ortho:  # Check if output_ortho is not empty
            for mistake in output_ortho:
                output_process.append((index, mistake))
    return output_process
