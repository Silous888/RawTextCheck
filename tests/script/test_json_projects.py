import unittest

from checkfrench.script import json_projects


class TestCreateID(unittest.TestCase):

    def test_create_id_empty(self) -> None:
        json_projects.data_json_projects = {}
        new_id: int = json_projects.create_id()
        self.assertEqual(new_id, 0)

    def test_create_id_non_empty(self) -> None:
        json_projects.data_json_projects = {
            0: {"id": 0},
            1: {"id": 1},
            5: {"id": 5}
        }
        new_id: int = json_projects.create_id()
        self.assertEqual(new_id, 6)


class TestCreateNewEntry(unittest.TestCase):

    def setUp(self) -> None:
        json_projects.data_json_projects = {}

    def test_create_new_entry_with_title_and_language(self) -> None:
        new_title = "My New Project"
        new_language = "fr"
        new_id: int = json_projects.create_new_entry(new_title, new_language)

        self.assertIn(new_id, json_projects.data_json_projects)
        entry: json_projects.Item = json_projects.data_json_projects[new_id]

        self.assertEqual(entry["id"], new_id)
        self.assertEqual(entry["title"], new_title)
        self.assertEqual(entry["language"], new_language)
        self.assertEqual(entry["path_dictionary"], "")
        self.assertEqual(entry["specific_argument"], "")
        self.assertEqual(entry["path_dictionary"], "")
        self.assertEqual(entry["valid_characters"], "")
        self.assertEqual(entry["ignored_codes_into_space"], [])
        self.assertEqual(entry["ignored_codes_into_nospace"], [])
        self.assertEqual(entry["ignored_substrings_space"], {})
        self.assertEqual(entry["ignored_substrings_nospace"], {})
        self.assertEqual(entry["ignored_rules_languagetool"], [])

    def test_create_multiple_entries(self) -> None:
        titles: list[str] = ["P1", "P2", "P3"]
        languages: list[str] = ["fr", "en", "de"]
        ids: list[int] = [json_projects.create_new_entry(t, l) for t, l in zip(titles, languages)]

        self.assertEqual(ids, [0, 1, 2])
        for i, (title, lang) in enumerate(zip(titles, languages)):
            self.assertIn(i, json_projects.data_json_projects)
            self.assertEqual(json_projects.data_json_projects[i]["title"], title)
            self.assertEqual(json_projects.data_json_projects[i]["language"], lang)

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

    def setUp(self) -> None:
        json_projects.data_json_projects = {
            0: {
                "id": 0,
                "title": "Test Project",
                "language": "fr",
                "parser": "sheet",
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
                "language": "fr",
                "parser": "sheet",
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
                "language": "fr",
                "parser": "sheet",
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
                "language": "fr",
                "parser": "sheet",
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
