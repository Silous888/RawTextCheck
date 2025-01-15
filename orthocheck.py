from pathlib import Path
import csv
from io import StringIO

CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àâäāéèêëēîïôöùûüÿçœæáȧāãčęīłṇñóøōõšṣṭúūžẓ"
    "ÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇŒÆÁȦĀÃČĘĪŁṆÑÓØŌÕŠṢṬÚŽẒ-"
)

dictionary_words: set[str] = set()


def parse_csv(csv_file: str) -> set[str]:
    """parse a dictionary file

    Args:
        csv_file (str): file to parse

    Returns:
        set[str]: words of the dictionary file
    """
    words: set[str] = set()
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            words.add(row[0].lower())
    return words


def load_words(folder_dict_name: str) -> None:
    """load all dictionary files

    Args:
        folder_dict_name (str): csv dictionaries folder

    Returns:
        set[str]: words from all dictionaries
    """
    global dictionary_words
    for path in Path(folder_dict_name).iterdir():
        if path.name.endswith('.csv'):
            dictionary_words = dictionary_words.union(parse_csv(str(path)))


def check_string(string: str) -> list[str]:
    """check if words if the string are in the dictionaries

    Args:
        string (str): string to check

    Returns:
        list[str]: words not in dictionary
    """
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
                    if word_to_check not in dictionary_words:
                        for sub_word in word_to_check.split('-'):
                            if sub_word not in dictionary_words:
                                output.append(word_to_check)
                                break
                else:
                    if word_to_check not in dictionary_words:
                        output.append(current_word)
                current_word = ""
        if char == "":
            break
        char = f.read(1)
    return output


def process_orthocheck(list_sentences: list[str]) -> list[tuple[int, str]]:
    """check if words are in dictionary for every strings

    Args:
        list_sentences (list[str]): strings to test

    Returns:
        list[tuple[int, str]]: words not in dictionary, with sentence index
    """
    output_process: list[tuple[int, str]] = []
    for index, sentence in enumerate(list_sentences):
        output_ortho: list[str] = check_string(sentence)
        if output_ortho:  # Check if output_ortho is not empty
            for mistake in output_ortho:
                output_process.append((index, mistake))
    return output_process
