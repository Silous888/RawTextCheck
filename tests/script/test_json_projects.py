import json
import os
import unittest

from checkfrench.script import json_projects
from checkfrench.default_parameters import JSON_FILE_PATH


def rename_json_during_test() -> None:
    """Safely rename the real json to backup and create a new empty one for testing."""
    if os.path.exists(JSON_FILE_PATH):
        os.rename(JSON_FILE_PATH, str(JSON_FILE_PATH) + ".bak")
    # Always create an empty JSON file for test
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)


def restore_json_after_test() -> None:
    """Restore the original json after the test, if backup exists"""
    if os.path.exists(JSON_FILE_PATH):
        os.remove(JSON_FILE_PATH)
    backup_path = str(JSON_FILE_PATH) + ".bak"
    if os.path.exists(backup_path):
        os.rename(backup_path, JSON_FILE_PATH)
    # Do not raise if backup does not exist; make test teardown safe


class TestCreateNewEntry(unittest.TestCase):

    def setUp(self) -> None:
        rename_json_during_test()

    def tearDown(self) -> None:
        restore_json_after_test()

    def test_create_new_entry_with_title_and_language(self) -> None:
        new_title = "My New Project"
        new_language = "fr"
        json_projects.create_new_entry(new_title, new_language)

        self.assertIn(new_title, json_projects.load_data())
        entry: json_projects.ItemProject = json_projects.load_data()[new_title]

        self.assertEqual(entry["language"], new_language)
        self.assertEqual(entry["parser"], "")
        self.assertEqual(entry["arg_parser"], "")
        self.assertEqual(entry["valid_characters"], "")
        self.assertEqual(entry["dictionary"], [])
        self.assertEqual(entry["banwords"], [])
        self.assertEqual(entry["ignored_codes_into_space"], [])
        self.assertEqual(entry["ignored_codes_into_nothing"], [])
        self.assertEqual(entry["ignored_substrings_into_space"], {})
        self.assertEqual(entry["ignored_substrings_into_nothing"], {})
        self.assertEqual(entry["ignored_rules"], [])
        self.assertEqual(entry["synchronized_path"], "")

    def test_create_multiple_entries(self) -> None:
        titles: list[str] = ["P1", "P2", "P3"]
        languages: list[str] = ["fr", "en", "de"]
        for title, lang in zip(titles, languages):
            json_projects.create_new_entry(title, lang)

        for title, lang in zip(titles, languages):
            self.assertIn(title, json_projects.load_data())
            entry: json_projects.ItemProject = json_projects.load_data()[title]
            self.assertEqual(entry["language"], lang)
            self.assertEqual(entry["parser"], "")
            self.assertEqual(entry["arg_parser"], "")
            self.assertEqual(entry["dictionary"], [])
            self.assertEqual(entry["valid_characters"], "")
            self.assertEqual(entry["banwords"], [])
            self.assertEqual(entry["ignored_codes_into_space"], [])
            self.assertEqual(entry["ignored_codes_into_nothing"], [])
            self.assertEqual(entry["ignored_substrings_into_space"], {})
            self.assertEqual(entry["ignored_substrings_into_nothing"], {})
            self.assertEqual(entry["ignored_rules"], [])
            self.assertEqual(entry["synchronized_path"], "")

    def test_create_entry_with_empty_title_should_fail(self) -> None:
        with self.assertRaises(ValueError):
            json_projects.create_new_entry("", "fr")

    def test_create_entry_with_empty_language_should_fail(self) -> None:
        with self.assertRaises(ValueError):
            json_projects.create_new_entry("My Project", "")


class TestAddValidCharacters(unittest.TestCase):

    base_valid_characters: list[str] = ["ABC123.,:!", ""]

    not_in_base_single: str = "D"
    not_in_base_multiple: str = "EF…?¿"
    in_base_single: str = "B"
    mix: str = "EF…?B¿"

    dangerous_characters: str = "\"\'\\/<>{}[]~`"

    title_id: list[str] = ["Test Project", "Test Project 2"]

    def setUp(self) -> None:
        rename_json_during_test()
        data: dict[str, json_projects.ItemProject] = {
            self.title_id[0]: {
                "language": "fr",
                "parser": "sheet",
                "arg_parser": "",
                "valid_characters": self.base_valid_characters[0],
                "dictionary": [],
                "banwords": [],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nothing": [],
                "ignored_substrings_into_space": {},
                "ignored_substrings_into_nothing": {},
                "ignored_rules": [],
                "synchronized_path": ""
            },
            self.title_id[1]: {
                "language": "fr",
                "parser": "sheet",
                "arg_parser": "",
                "valid_characters": self.base_valid_characters[1],
                "dictionary": [],
                "banwords": [],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nothing": [],
                "ignored_substrings_into_space": {},
                "ignored_substrings_into_nothing": {},
                "ignored_rules": [],
                "synchronized_path": ""
            }
        }
        json_projects.save_data(data)

    def tearDown(self) -> None:
        restore_json_after_test()

    def test_add_single_new_char(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.add_valid_characters(id_dict, self.not_in_base_single)
            data = json_projects.load_data()
            self.assertIn(self.not_in_base_single,
                          data[id_dict]["valid_characters"])
            self.assertEqual(data[id_dict]["valid_characters"],
                             self.base_valid_characters[self.title_id.index(id_dict)]
                             + self.not_in_base_single)

    def test_add_multiple_new_chars(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.add_valid_characters(id_dict, self.not_in_base_multiple)
            data = json_projects.load_data()
            for char in self.not_in_base_multiple:
                self.assertIn(char,
                              data[id_dict]["valid_characters"])
            self.assertEqual(data[id_dict]["valid_characters"],
                             self.base_valid_characters[self.title_id.index(id_dict)]
                             + self.not_in_base_multiple)

    def test_add_existing_char(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        json_projects.add_valid_characters("", self.in_base_single)
        data = json_projects.load_data()
        self.assertEqual(data[self.title_id[0]]["valid_characters"],
                         self.base_valid_characters[0])

    def test_add_mixed_existing_and_new_chars(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        json_projects.add_valid_characters(self.title_id[0], self.mix)
        data = json_projects.load_data()
        for char in self.not_in_base_multiple:
            self.assertIn(char, data[self.title_id[0]]["valid_characters"])
            self.assertEqual(data[self.title_id[0]]["valid_characters"].count(char), 1)
        self.assertEqual(data[self.title_id[0]]["valid_characters"],
                         self.base_valid_characters[0] + self.not_in_base_multiple)

    def test_add_empty_string(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.add_valid_characters(id_dict, "")
            data = json_projects.load_data()
            self.assertEqual(data[id_dict]["valid_characters"],
                             self.base_valid_characters[self.title_id.index(id_dict)])

    def test_add_dangerous_char(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.add_valid_characters(id_dict, self.dangerous_characters)
            data = json_projects.load_data()
            for char in self.dangerous_characters:
                self.assertIn(char, data[id_dict]["valid_characters"])
            self.assertEqual(data[id_dict]["valid_characters"],
                             self.base_valid_characters[self.title_id.index(id_dict)] + self.dangerous_characters)


class TestSetValidCharacters(unittest.TestCase):

    new_valid_characters: str = "XYZ789,.:!"

    title_id: list[str] = ["Test Project", "Test Project 2"]

    def setUp(self) -> None:
        rename_json_during_test()
        data: dict[str, json_projects.ItemProject] = {
            self.title_id[0]: {
                "language": "fr",
                "parser": "sheet",
                "arg_parser": "",
                "valid_characters": "ABC123.,:!",
                "dictionary": [],
                "banwords": [],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nothing": [],
                "ignored_substrings_into_space": {},
                "ignored_substrings_into_nothing": {},
                "ignored_rules": [],
                "synchronized_path": ""
            },
            self.title_id[1]: {
                "language": "fr",
                "parser": "sheet",
                "arg_parser": "",
                "valid_characters": "",
                "dictionary": [],
                "banwords": [],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nothing": [],
                "ignored_substrings_into_space": {},
                "ignored_substrings_into_nothing": {},
                "ignored_rules": [],
                "synchronized_path": ""
            }
        }
        json_projects.save_data(data)

    def tearDown(self) -> None:
        restore_json_after_test()

    def test_with_characters_already(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.set_valid_characters(id_dict, self.new_valid_characters)
            data = json_projects.load_data()
            self.assertEqual(data[id_dict]["valid_characters"],
                             self.new_valid_characters)

    def test_with_empty_string(self) -> None:
        data: dict[str, json_projects.ItemProject] = json_projects.load_data()
        for id_dict in data:
            json_projects.set_valid_characters(id_dict, "")
            data = json_projects.load_data()
            self.assertEqual(data[id_dict]["valid_characters"],
                             "")


if __name__ == "__main__":
    unittest.main()
