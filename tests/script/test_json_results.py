import tempfile
import unittest

from rawtextcheck.script import json_results


class TestJsonResults(unittest.TestCase):
    def setUp(self) -> None:
        # create a temporary directory for RESULTS_FOLDER_PATH
        self.test_dir = tempfile.TemporaryDirectory()
        json_results.RESULTS_FOLDER = self.test_dir.name

        self.project_title = "TestProject"
        self.file_name = "results.json"

        self.sample_data: list[json_results.ItemResult] = [
            {
                "line_number": "1",
                "line": "Ceci est une ligne.",
                "error": "Erreur A",
                "error_type": "TypeA",
                "explanation": "Explication A"
            },
            {
                "line_number": "3",
                "line": "Une autre ligne",
                "error": "Erreur B",
                "error_type": "TypeB",
                "explanation": "Explication B"
            },
            {
                "line_number": "3",
                "line": "Encore une autre ligne",
                "error": "Erreur C",
                "error_type": "TypeB",
                "explanation": "Explication C"
            }
        ]

        self.generated_data: dict[str, json_results.ItemResult] = json_results.generate_id_errors(self.sample_data)

        # save generated data
        json_results.save_data(self.project_title, self.file_name, self.generated_data)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_generate_id_errors(self) -> None:
        ids = list(self.generated_data.keys())
        self.assertIn("1a", ids)
        self.assertIn("3a", ids)
        self.assertIn("3b", ids)
        self.assertEqual(len(ids), 3)
        # ensure unique keys
        self.assertEqual(len(set(ids)), len(ids))

    def test_delete_error_type(self) -> None:
        json_results.delete_error_type(self.project_title, self.file_name, "TypeB")
        data: dict[str, json_results.ItemResult] = json_results.get_file_data(self.project_title, self.file_name)
        self.assertEqual(len(data), 1)
        for item in data.values():
            self.assertNotEqual(item["error_type"], "TypeB")

    def test_delete_specific_error_with_type(self) -> None:
        # Delete only "Erreur C" with "TypeB"
        json_results.delete_specific_error_with_type(self.project_title, self.file_name, "TypeB", "Erreur C")
        data: dict[str, json_results.ItemResult] = json_results.get_file_data(self.project_title, self.file_name)

        # There should be 2 errors remaining: 1 from TypeA, 1 from TypeB (Erreur B)
        self.assertEqual(len(data), 2)
        for item in data.values():
            self.assertFalse(item["error"] == "Erreur C" and item["error_type"] == "TypeB")


if __name__ == "__main__":
    unittest.main()
