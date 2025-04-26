import unittest

from checkfrench.script import json_projects


class TestAddValidCharacters(unittest.TestCase):

    base_valid_characters: list[str] = ["ABC123.,:!", ""]

    not_in_base_single: str = "D"
    not_in_base_multiple: str = "EF…?¿"
    in_base_single: str = "B"
    mix: str = "EF…?B¿"

    dangerous_characters: str = "\"\'\\/<>{}[]~`"

    def setUp(self) -> None:
        json_projects.data_json_projects = {
            0: {
                "id": 0,
                "title": "Test Project",
                "folder_name": "Test Folder",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_characters": self.base_valid_characters[0],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            },
            1: {
                "id": 1,
                "title": "Test Project 2",
                "folder_name": "Test Folder 2",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_characters": self.base_valid_characters[1],
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            }
        }

    def test_add_single_new_char(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.add_valid_characters(id_dict, self.not_in_base_single)
            self.assertIn(self.not_in_base_single,
                          json_projects.data_json_projects[id_dict]["valid_characters"])
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             self.base_valid_characters[id_dict] + self.not_in_base_single)

    def test_add_multiple_new_chars(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.add_valid_characters(id_dict, self.not_in_base_multiple)
            for char in self.not_in_base_multiple:
                self.assertIn(char,
                              json_projects.data_json_projects[id_dict]["valid_characters"])
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             self.base_valid_characters[id_dict] + self.not_in_base_multiple)

    def test_add_existing_char(self) -> None:
        json_projects.add_valid_characters(0, self.in_base_single)
        self.assertEqual(json_projects.data_json_projects[0]["valid_characters"],
                         self.base_valid_characters[0])

    def test_add_mixed_existing_and_new_chars(self) -> None:
        json_projects.add_valid_characters(0, self.mix)
        for char in self.not_in_base_multiple:
            self.assertIn(char, json_projects.data_json_projects[0]["valid_characters"])
            self.assertEqual(json_projects.data_json_projects[0]["valid_characters"].count(char), 1)
        self.assertEqual(json_projects.data_json_projects[0]["valid_characters"],
                         self.base_valid_characters[0] + self.not_in_base_multiple)

    def test_add_empty_string(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.add_valid_characters(id_dict, "")
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             self.base_valid_characters[id_dict])

    def test_add_dangerous_char(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.add_valid_characters(id_dict, self.dangerous_characters)
            for char in self.dangerous_characters:
                self.assertIn(char, json_projects.data_json_projects[id_dict]["valid_characters"])
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             self.base_valid_characters[id_dict] + self.dangerous_characters)


class TestSetValidCharacters(unittest.TestCase):

    new_valid_characters: str = "XYZ789,.:!"

    def setUp(self) -> None:
        json_projects.data_json_projects = {
            0: {
                "id": 0,
                "title": "Test Project",
                "folder_name": "Test Folder",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_characters": "ABC123.,:!",
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            },
            1: {
                "id": 1,
                "title": "Test Project 2",
                "folder_name": "Test Folder 2",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_characters": "",
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            }
        }

    def test_with_characters_already(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.set_valid_characters(id_dict, self.new_valid_characters)
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             self.new_valid_characters)

    def test_with_empty_string(self) -> None:
        for id_dict in json_projects.data_json_projects:
            json_projects.set_valid_characters(id_dict, "")
            self.assertEqual(json_projects.data_json_projects[id_dict]["valid_characters"],
                             "")


if __name__ == "__main__":
    unittest.main()
