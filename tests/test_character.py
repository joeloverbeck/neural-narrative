import logging
from unittest.mock import patch, MagicMock

import pytest

from src.characters.character import Character


# Fixture for character data with all required attributes
@pytest.fixture
def character_data():
    return {
        "name": "Test Character",
        "description": "A character used for testing.",
        "personality": "Testy",
        "profile": "Test Profile",
        "likes": "Testing",
        "dislikes": "Not testing",
        "secrets": "No secrets",
        "speech_patterns": "Test speech",
        "health": "Healthy",
        "equipment": "Test equipment",
        "voice_gender": "Neutral",
        "voice_age": "Adult",
        "voice_emotion": "Neutral",
        "voice_tempo": "Normal",
        "voice_volume": "Medium",
        "voice_tone": "Normal",
        "voice_texture": "Smooth",
        "voice_style": "Conversational",
        "voice_personality": "Friendly",
        "voice_special_effects": "None",
        "voice_model": "Test Model",
    }


# Fixture for the characters file containing character data
@pytest.fixture
def characters_file(character_data):
    return {"test_character": character_data}


def test_character_initialization(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.name == "Test Character"
            assert character.description == "A character used for testing."
            assert character.personality == "Testy"
            assert character.health == "Healthy"


def test_character_initialization_missing_attributes(characters_file):
    # Remove a required attribute
    del characters_file["test_character"]["name"]

    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            with pytest.raises(KeyError) as excinfo:
                Character("test_playthrough", "test_character", mock_fs_manager)
            assert "missing the following required attributes: name" in str(
                excinfo.value
            )


def test_character_initialization_identifier_not_found(characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            with pytest.raises(KeyError) as excinfo:
                Character("test_playthrough", "nonexistent_character", mock_fs_manager)
            assert (
                "Character with identifier 'nonexistent_character' not found."
                in str(excinfo.value)
            )


def test_get_attribute(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)
            assert character.get_attribute("name") == "Test Character"
            assert character.get_attribute("nonexistent_attribute") is None


def test_update_data(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            updated_data = {
                "description": "An updated description.",
                "new_field": "Should be ignored",
            }
            character.update_data(updated_data)

            assert character.description == "An updated description."
            assert "new_field" not in character._data


def test_update_data_with_invalid_field(character_data, characters_file, caplog):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            with caplog.at_level(logging.WARNING):
                updated_data = {"nonexistent_field": "value"}
                character.update_data(updated_data)
                assert "Ignored character attribute" in caplog.text


def test_update_data_with_empty_data(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            with pytest.raises(ValueError) as excinfo:
                character.update_data({})
            assert "updated_data can't be empty." in str(excinfo.value)


def test_save_method(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            character.save()

            mock_fs_manager.save_json_file.assert_called_once_with(
                characters_file, "path/to/characters.json"
            )


def test_character_properties(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.get_file_path_to_character_image_for_web.return_value = (
                "path/to/image.png"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.name == "Test Character"
            assert character.description == "A character used for testing."
            assert character.image_url == "path/to/image.png"


def test_has_description_for_portrait_true(character_data, characters_file):
    character_data["description_for_portrait"] = "A description for portrait."

    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.has_description_for_portrait() is True
            assert character.description_for_portrait == "A description for portrait."


def test_has_description_for_portrait_false(character_data, characters_file):
    if "description_for_portrait" in character_data:
        del character_data["description_for_portrait"]

    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.has_description_for_portrait() is False


def test_description_for_portrait_missing(character_data, characters_file):
    if "description_for_portrait" in character_data:
        del character_data["description_for_portrait"]

    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            with pytest.raises(KeyError):
                _ = character.description_for_portrait


def test_update_multiple_fields(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            updated_data = {
                "description": "An updated description.",
                "likes": "New likes",
                "dislikes": "New dislikes",
            }
            character.update_data(updated_data)

            assert character.description == "An updated description."
            assert character.likes == "New likes"
            assert character.dislikes == "New dislikes"


def test_update_data_calls_save(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            character.save = MagicMock()

            updated_data = {"description": "An updated description."}
            character.update_data(updated_data)

            character.save.assert_called_once()


def test_save_updates_characters_file(character_data, characters_file):
    updated_characters_file = characters_file.copy()
    updated_characters_file["test_character"]["description"] = "An updated description."

    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.save_json_file = MagicMock()

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            character.update_data({"description": "An updated description."})

            mock_fs_manager.save_json_file.assert_called_once_with(
                updated_characters_file, "path/to/characters.json"
            )


def test_image_url_property(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )
            mock_fs_manager.get_file_path_to_character_image_for_web.return_value = (
                "path/to/image.png"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.image_url == "path/to/image.png"

            mock_fs_manager.get_file_path_to_character_image_for_web.assert_called_once_with(
                "test_playthrough", "test_character"
            )


def test_identifier_property(character_data, characters_file):
    with patch("src.characters.character.read_json_file") as mock_read_json_file:
        mock_read_json_file.return_value = characters_file

        with patch(
            "src.filesystem.filesystem_manager.FilesystemManager"
        ) as MockFilesystemManager:
            mock_fs_manager = MockFilesystemManager.return_value
            mock_fs_manager.get_file_path_to_characters_file.return_value = (
                "path/to/characters.json"
            )

            character = Character("test_playthrough", "test_character", mock_fs_manager)

            assert character.identifier == "test_character"
