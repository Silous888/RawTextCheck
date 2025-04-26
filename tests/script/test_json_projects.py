import unittest

from checkfrench.script import json_projects


class TestAddValidAlphanumeric(unittest.TestCase):

    base_valid_alphanumeric: str = "ABC123"

    not_in_base_single: str = "D"
    not_in_base_multiple: str = "EF"
    in_base: str = "A"
    mix: str = "EAF"

    def setUp(self) -> None:
        json_projects.data_json_projects = {
            1: {
                "id": 1,
                "title": "Test Project",
                "folder_name": "Test Folder",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_alphanumeric": self.base_valid_alphanumeric,
                "valid_punctuation": "",
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            }
        }

    def test_add_single_new_char(self) -> None:
        json_projects.add_valid_alphanumeric(1, self.not_in_base_single)
        self.assertIn(self.not_in_base_single, json_projects.data_json_projects[1]["valid_alphanumeric"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"],
                         self.base_valid_alphanumeric + self.not_in_base_single)

    def test_add_multiple_new_chars(self) -> None:
        json_projects.add_valid_alphanumeric(1, self.not_in_base_multiple)
        for char in self.not_in_base_multiple:
            self.assertIn(char, json_projects.data_json_projects[1]["valid_alphanumeric"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"],
                         self.base_valid_alphanumeric + self.not_in_base_multiple)

    def test_add_existing_char(self) -> None:
        json_projects.add_valid_alphanumeric(1, self.in_base)
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"], self.base_valid_alphanumeric)

    def test_add_mixed_existing_and_new_chars(self) -> None:
        json_projects.add_valid_alphanumeric(1, self.mix)
        for char in self.not_in_base_multiple:
            self.assertIn(char, json_projects.data_json_projects[1]["valid_alphanumeric"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"].count(self.in_base),
                         self.base_valid_alphanumeric.count(self.in_base))
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"],
                         self.base_valid_alphanumeric + self.not_in_base_multiple)

    def test_add_empty_string(self) -> None:
        json_projects.add_valid_alphanumeric(1, "")
        self.assertEqual(json_projects.data_json_projects[1]["valid_alphanumeric"], self.base_valid_alphanumeric)


class TestAddValidPunctuation(unittest.TestCase):

    base_valid_punctuation: str = ".,:!"

    not_in_base_single: str = "…"
    not_in_base_multiple: str = "…?¿"
    in_base: str = ","
    mix: str = "…?,¿"
    dangerous_char: str = "\"\'\\/<>{}[]~`"

    def setUp(self) -> None:
        json_projects.data_json_projects = {
            1: {
                "id": 1,
                "title": "Test Project",
                "folder_name": "Test Folder",
                "specific_argument": "",
                "path_dictionary": "",
                "valid_alphanumeric": "",
                "valid_punctuation": self.base_valid_punctuation,
                "ignored_codes_into_space": [],
                "ignored_codes_into_nospace": [],
                "ignored_substrings_space": {},
                "ignored_substrings_nospace": {},
                "ignored_rules_languagetool": []
            }
        }

    def test_add_single_new_char(self) -> None:
        json_projects.add_valid_punctuation(1, self.not_in_base_single)
        self.assertIn(self.not_in_base_single, json_projects.data_json_projects[1]["valid_punctuation"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"],
                         self.base_valid_punctuation + self.not_in_base_single)

    def test_add_multiple_new_chars(self) -> None:
        json_projects.add_valid_punctuation(1, self.not_in_base_multiple)
        for char in self.not_in_base_multiple:
            self.assertIn(char, json_projects.data_json_projects[1]["valid_punctuation"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"],
                         self.base_valid_punctuation + self.not_in_base_multiple)

    def test_add_existing_char(self) -> None:
        json_projects.add_valid_punctuation(1, self.in_base)
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"], self.base_valid_punctuation)

    def test_add_mixed_existing_and_new_chars(self) -> None:
        json_projects.add_valid_punctuation(1, self.mix)
        for char in self.not_in_base_multiple:
            self.assertIn(char, json_projects.data_json_projects[1]["valid_punctuation"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"].count(self.in_base),
                         self.base_valid_punctuation.count(self.in_base))
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"],
                         self.base_valid_punctuation + self.not_in_base_multiple)

    def test_add_empty_string(self) -> None:
        json_projects.add_valid_punctuation(1, "")
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"], self.base_valid_punctuation)

    def test_add_dangerous_char(self) -> None:
        json_projects.add_valid_punctuation(1, self.dangerous_char)
        for char in self.dangerous_char:
            self.assertIn(char, json_projects.data_json_projects[1]["valid_punctuation"])
        self.assertEqual(json_projects.data_json_projects[1]["valid_punctuation"],
                         self.base_valid_punctuation + self.dangerous_char)


if __name__ == "__main__":
    unittest.main()
