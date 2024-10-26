import unittest
from unittest.mock import patch

from src.characters.character_guidelines_manager import CharacterGuidelinesManager


class TestCharacterGuidelinesManager(unittest.TestCase):

    def setUp(self):
        # Start patching read_json_file
        self.patcher_read = patch(
            "src.characters.character_guidelines_manager.read_json_file"
        )
        self.mock_read_json_file = self.patcher_read.start()

        # Start patching write_json_file
        self.patcher_write = patch(
            "src.characters.character_guidelines_manager.write_json_file"
        )
        self.mock_write_json_file = self.patcher_write.start()

        # Ensure that write_json_file doesn't perform any real file operations
        self.mock_write_json_file.return_value = None

        # Set up a default guidelines file content
        self.guidelines_content = {
            "universe1:world1:region1:area1": ["Guideline 1", "Guideline 2"],
            "universe1:world1:region1:area1:location1": ["Guideline A"],
        }
        self.mock_read_json_file.return_value = self.guidelines_content.copy()

        # Initialize the CharacterGuidelinesManager
        self.manager = CharacterGuidelinesManager()

    def tearDown(self):
        # Stop all patches
        patch.stopall()

    def test_create_key_with_location(self):
        key = self.manager.create_key(
            "universe1", "world1", "region1", "area1", "location1"
        )
        self.assertEqual(key, "universe1:world1:region1:area1:location1")

    def test_create_key_without_location(self):
        key = self.manager.create_key("universe1", "world1", "region1", "area1")
        self.assertEqual(key, "universe1:world1:region1:area1")

    def test_load_guidelines_existing_key(self):
        guidelines = self.manager.load_guidelines(
            "universe1", "world1", "region1", "area1"
        )
        self.assertEqual(guidelines, ["Guideline 1", "Guideline 2"])

    def test_load_guidelines_non_existing_key(self):
        with self.assertRaises(ValueError):
            self.manager.load_guidelines("universe2", "world2", "region2", "area2")

    @patch("src.characters.character_guidelines_manager.validate_non_empty_string")
    def test_save_guidelines_new_key(self, mock_validate):
        guidelines_to_save = ["New Guideline 1", "New Guideline 2"]
        self.manager.save_guidelines(
            "universe2", "world2", "region2", "area2", guidelines_to_save
        )
        key = "universe2:world2:region2:area2"
        self.assertIn(key, self.manager._guidelines_file)
        self.assertEqual(self.manager._guidelines_file[key], guidelines_to_save)
        # Ensure validate_non_empty_string was called for each guideline
        self.assertEqual(mock_validate.call_count, len(guidelines_to_save))
        # Ensure _save_guidelines_file() was called
        self.mock_write_json_file.assert_called_once()

    @patch("src.characters.character_guidelines_manager.validate_non_empty_string")
    def test_save_guidelines_existing_key(self, mock_validate):
        guidelines_to_save = ["Additional Guideline"]
        self.manager.save_guidelines(
            "universe1", "world1", "region1", "area1", guidelines_to_save
        )
        key = "universe1:world1:region1:area1"
        self.assertIn(key, self.manager._guidelines_file)
        self.assertEqual(
            self.manager._guidelines_file[key],
            ["Guideline 1", "Guideline 2", "Additional Guideline"],
        )
        # Ensure validate_non_empty_string was called for each guideline
        self.assertEqual(mock_validate.call_count, len(guidelines_to_save))
        # Ensure _save_guidelines_file() was called
        self.mock_write_json_file.assert_called_once()

    def test_guidelines_exist_true(self):
        exists = self.manager.guidelines_exist(
            "universe1", "world1", "region1", "area1"
        )
        self.assertTrue(exists)

    def test_guidelines_exist_false(self):
        exists = self.manager.guidelines_exist(
            "universe2", "world2", "region2", "area2"
        )
        self.assertFalse(exists)

    @patch("src.characters.character_guidelines_manager.validate_non_empty_string")
    def test_validate_non_empty_string_called(self, mock_validate):
        guidelines_to_save = ["Guideline X", "Guideline Y"]
        self.manager.save_guidelines(
            "universe3", "world3", "region3", "area3", guidelines_to_save
        )
        # Ensure validate_non_empty_string was called for each guideline
        expected_calls = [
            unittest.mock.call("Guideline X", "guideline"),
            unittest.mock.call("Guideline Y", "guideline"),
        ]
        mock_validate.assert_has_calls(expected_calls, any_order=True)

    @patch("src.characters.character_guidelines_manager.validate_non_empty_string")
    def test_save_guidelines_empty_guideline(self, mock_validate):
        mock_validate.side_effect = ValueError("Guideline cannot be empty.")
        with self.assertRaises(ValueError):
            self.manager.save_guidelines(
                "universe4", "world4", "region4", "area4", [""]
            )
        # Ensure validate_non_empty_string was called
        mock_validate.assert_called_once_with("", "guideline")


if __name__ == "__main__":
    unittest.main()
