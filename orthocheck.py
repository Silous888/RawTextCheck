from pathlib import Path
import csv
from io import StringIO

CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

dictionary_words: set[str] = set()

dictionary_specific: set[str] = set()

full_dictionary: set[str] = set()


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


def check_string(string: str, correct_char: str, correct_punct: str) -> list[str]:
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
        if char not in (CHARS + correct_char + correct_punct) and char != "":
            if char not in correct_punct and char != "":
                output.append(char + " => caractère non autorisé")
            else:
                output.append(char + " => ponctuation non autorisée")
        if char in (CHARS + correct_char) and char != "":
            current_word += char
        else:
            if current_word != "":
                word_to_check = current_word.lower()

                if "-" in word_to_check:
                    if word_to_check not in full_dictionary:
                        for sub_word in word_to_check.split('-'):
                            if sub_word not in full_dictionary:
                                output.append(word_to_check)
                                break
                else:
                    if word_to_check not in full_dictionary:
                        output.append(current_word)
                current_word = ""
        if char == "":
            break
        char = f.read(1)
    return output


def process_orthocheck(list_sentences: list[str], list_specific_words: list[str],
                       correct_char: str, correct_punct: str) -> list[tuple[int, str]]:
    """check if words are in dictionary for every strings

    Args:
        list_sentences (list[str]): strings to test

    Returns:
        list[tuple[int, str]]: words not in dictionary, with sentence index
    """
    global dictionary_specific, full_dictionary
    dictionary_specific = set([word.lower() for word in list_specific_words])
    full_dictionary = dictionary_words.union(dictionary_specific)
    output_process: list[tuple[int, str]] = []
    for index, sentence in enumerate(list_sentences):
        output_ortho: list[str] = check_string(sentence, correct_char, correct_punct)
        if output_ortho:  # Check if output_ortho is not empty
            for mistake in output_ortho:
                output_process.append((index + 1, mistake))
    return output_process
