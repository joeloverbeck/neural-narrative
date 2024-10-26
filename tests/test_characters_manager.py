from pathlib import Path
from unittest.mock import Mock, patch, call

import pytest

from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
# Assuming the classes are available for import
from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager


# Test __init__


def test_characters_manager_init_with_valid_parameters():
    # Arrange
    playthrough_name = "test_playthrough"
    filesystem_manager = Mock(spec=FilesystemManager)
    identifiers_manager = Mock(spec=IdentifiersManager)
    playthrough_manager = Mock(spec=PlaythroughManager)

    # Act
    manager = CharactersManager(
        playthrough_name=playthrough_name,
        filesystem_manager=filesystem_manager,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )

    # Assert
    assert manager._playthrough_name == playthrough_name
    assert manager._filesystem_manager == filesystem_manager
    assert manager._identifiers_manager == identifiers_manager
    assert manager._playthrough_manager == playthrough_manager


def test_characters_manager_init_with_empty_playthrough_name():
    # Arrange
    playthrough_name = ""
    # Act & Assert
    with pytest.raises(ValueError):
        CharactersManager(playthrough_name=playthrough_name)


def test_characters_manager_init_creates_default_managers():
    # Arrange
    playthrough_name = "test_playthrough"

    with patch(
        "src.characters.characters_manager.FilesystemManager"
    ) as MockFilesystemManager, patch(
        "src.characters.characters_manager.IdentifiersManager"
    ) as MockIdentifiersManager, patch(
        "src.characters.characters_manager.PlaythroughManager"
    ) as MockPlaythroughManager:
        mock_filesystem_manager_instance = MockFilesystemManager.return_value
        mock_identifiers_manager_instance = MockIdentifiersManager.return_value
        mock_playthrough_manager_instance = MockPlaythroughManager.return_value

        # Act
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Assert
        MockFilesystemManager.assert_called_once()
        MockIdentifiersManager.assert_called_once_with(playthrough_name)
        MockPlaythroughManager.assert_called_once_with(playthrough_name)
        assert manager._filesystem_manager == mock_filesystem_manager_instance
        assert manager._identifiers_manager == mock_identifiers_manager_instance
        assert manager._playthrough_manager == mock_playthrough_manager_instance


# Test _load_characters_file


def test_load_characters_file():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {
        "char1": {"name": "Character One"},
        "char2": {"name": "Character Two"},
    }
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.get_file_path_to_characters_file.return_value = (
        "/path/to/characters.json"
    )

    with patch(
        "src.characters.characters_manager.read_json_file", return_value=characters_data
    ) as mock_read_json_file:
        manager = CharactersManager(
            playthrough_name=playthrough_name, filesystem_manager=filesystem_manager
        )

        # Act
        result = manager._load_characters_file()

        # Assert
        filesystem_manager.get_file_path_to_characters_file.assert_called_once_with(
            playthrough_name
        )
        mock_read_json_file.assert_called_once_with(Path("/path/to/characters.json"))
        assert result == characters_data


# Test _load_map_file


def test_load_map_file():
    # Arrange
    playthrough_name = "test_playthrough"
    map_data = {"place1": {"characters": ["char1", "char2"]}}
    filesystem_manager = Mock(spec=FilesystemManager)
    filesystem_manager.get_file_path_to_map.return_value = "/path/to/map.json"

    with patch(
        "src.characters.characters_manager.read_json_file", return_value=map_data
    ) as mock_read_json_file:
        manager = CharactersManager(
            playthrough_name=playthrough_name, filesystem_manager=filesystem_manager
        )

        # Act
        result = manager._load_map_file()

        # Assert
        filesystem_manager.get_file_path_to_map.assert_called_once_with(
            playthrough_name
        )
        mock_read_json_file.assert_called_once_with(Path("/path/to/map.json"))
        assert result == map_data


# Test get_latest_character_identifier


def test_get_latest_character_identifier():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {"char1": {}, "char2": {}, "char3": {}}
    filesystem_manager = Mock(spec=FilesystemManager)
    identifiers_manager = Mock(spec=IdentifiersManager)
    identifiers_manager.get_highest_identifier.return_value = "char3"

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ) as mock_load_characters_file:
        manager = CharactersManager(
            playthrough_name=playthrough_name,
            filesystem_manager=filesystem_manager,
            identifiers_manager=identifiers_manager,
        )

        # Act
        result = manager.get_latest_character_identifier()

        # Assert
        mock_load_characters_file.assert_called_once()
        identifiers_manager.get_highest_identifier.assert_called_once_with(
            characters_data
        )
        assert result == "char3"


# Test get_characters


def test_get_characters():
    # Arrange
    playthrough_name = "test_playthrough"
    character_identifiers = ["char1", "char2"]
    filesystem_manager = Mock(spec=FilesystemManager)
    character_instance1 = Mock(spec=Character)
    character_instance2 = Mock(spec=Character)

    with patch(
        "src.characters.characters_manager.Character",
        side_effect=[character_instance1, character_instance2],
    ) as mock_character:
        manager = CharactersManager(
            playthrough_name=playthrough_name, filesystem_manager=filesystem_manager
        )

        # Act
        result = manager.get_characters(character_identifiers)

        # Assert
        calls = [
            call(playthrough_name, "char1"),
            call(playthrough_name, "char2"),
        ]
        mock_character.assert_has_calls(calls, any_order=False)
        assert result == [character_instance1, character_instance2]


# Test get_followers


def test_get_followers():
    # Arrange
    playthrough_name = "test_playthrough"
    followers = ["char1", "char2"]
    character_instance1 = Mock(spec=Character)
    character_instance2 = Mock(spec=Character)
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_followers.return_value = followers

    with patch(
        "src.characters.characters_manager.Character",
        side_effect=[character_instance1, character_instance2],
    ) as mock_character:
        manager = CharactersManager(
            playthrough_name=playthrough_name, playthrough_manager=playthrough_manager
        )

        # Act
        result = manager.get_followers()

        # Assert
        playthrough_manager.get_followers.assert_called_once()
        calls = [
            call(playthrough_name, "char1"),
            call(playthrough_name, "char2"),
        ]
        mock_character.assert_has_calls(calls, any_order=False)
        assert result == [character_instance1, character_instance2]


# Test get_characters_at_current_place


def test_get_characters_at_current_place():
    # Arrange
    playthrough_name = "test_playthrough"
    current_place_identifier = "place1"
    character_ids = ["char1", "char2"]
    map_data = {current_place_identifier: {"characters": character_ids}}
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    character_instance1 = Mock(spec=Character)
    character_instance2 = Mock(spec=Character)

    with patch.object(
        CharactersManager, "_load_map_file", return_value=map_data
    ) as mock_load_map_file, patch(
        "src.characters.characters_manager.Character",
        side_effect=[character_instance1, character_instance2],
    ) as mock_character:
        manager = CharactersManager(
            playthrough_name=playthrough_name, playthrough_manager=playthrough_manager
        )

        # Act
        result = manager.get_characters_at_current_place()

        # Assert
        playthrough_manager.get_current_place_identifier.assert_called_once()
        mock_load_map_file.assert_called_once()
        calls = [
            call(playthrough_name, "char1"),
            call(playthrough_name, "char2"),
        ]
        mock_character.assert_has_calls(calls, any_order=False)
        assert result == [character_instance1, character_instance2]


def test_get_characters_at_current_place_no_characters():
    # Arrange
    playthrough_name = "test_playthrough"
    current_place_identifier = "place1"
    map_data = {current_place_identifier: {}}
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    with patch.object(CharactersManager, "_load_map_file", return_value=map_data):
        manager = CharactersManager(
            playthrough_name=playthrough_name, playthrough_manager=playthrough_manager
        )

        # Act
        result = manager.get_characters_at_current_place()

        # Assert
        assert result == []


# Test get_all_characters


def test_get_all_characters():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {
        "char1": {"name": "Character One"},
        "char2": {"name": "Character Two"},
        "char3": {},
    }
    expected_result = [
        {"identifier": "char1", "name": "Character One"},
        {"identifier": "char2", "name": "Character Two"},
        {"identifier": "char3", "name": "Unknown"},
    ]

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ) as mock_load_characters_file:
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Act
        result = manager.get_all_characters()

        # Assert
        mock_load_characters_file.assert_called_once()
        assert result == expected_result


def test_get_all_characters_empty_characters_file():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {}

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ):
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Act
        result = manager.get_all_characters()

        # Assert
        assert result == []


# Test get_all_character_names


def test_get_all_character_names():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {
        "char1": {"name": "Character One"},
        "char2": {"name": "Character Two"},
        "char3": {"name": ""},
    }
    expected_result = ["Character One", "Character Two", ""]

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ) as mock_load_characters_file:
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Act
        result = manager.get_all_character_names()

        # Assert
        mock_load_characters_file.assert_called_once()
        assert result == expected_result


def test_get_all_character_names_empty_characters_file():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {}

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ):
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Act
        result = manager.get_all_character_names()

        # Assert
        assert result == []


# Edge case tests


def test_get_latest_character_identifier_no_characters():
    # Arrange
    playthrough_name = "test_playthrough"
    characters_data = {}
    filesystem_manager = Mock(spec=FilesystemManager)
    identifiers_manager = Mock(spec=IdentifiersManager)
    identifiers_manager.get_highest_identifier.return_value = None

    with patch.object(
        CharactersManager, "_load_characters_file", return_value=characters_data
    ):
        manager = CharactersManager(
            playthrough_name=playthrough_name,
            filesystem_manager=filesystem_manager,
            identifiers_manager=identifiers_manager,
        )

        # Act
        result = manager.get_latest_character_identifier()

        # Assert
        identifiers_manager.get_highest_identifier.assert_called_once_with(
            characters_data
        )
        assert result is None


def test_get_followers_no_followers():
    # Arrange
    playthrough_name = "test_playthrough"
    followers = []
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_followers.return_value = followers

    with patch("src.characters.characters_manager.Character") as mock_character:
        manager = CharactersManager(
            playthrough_name=playthrough_name, playthrough_manager=playthrough_manager
        )

        # Act
        result = manager.get_followers()

        # Assert
        playthrough_manager.get_followers.assert_called_once()
        mock_character.assert_not_called()
        assert result == []


def test_get_characters_with_empty_list():
    # Arrange
    playthrough_name = "test_playthrough"
    character_identifiers = []
    filesystem_manager = Mock(spec=FilesystemManager)

    with patch("src.characters.characters_manager.Character") as mock_character:
        manager = CharactersManager(
            playthrough_name=playthrough_name, filesystem_manager=filesystem_manager
        )

        # Act
        result = manager.get_characters(character_identifiers)

        # Assert
        mock_character.assert_not_called()
        assert result == []


def test_get_characters_at_current_place_plus_followers_no_characters_no_followers():
    # Arrange
    playthrough_name = "test_playthrough"

    with patch.object(
        CharactersManager, "get_characters_at_current_place", return_value=[]
    ) as mock_get_characters_at_current_place, patch.object(
        CharactersManager, "get_followers", return_value=[]
    ) as mock_get_followers:
        manager = CharactersManager(playthrough_name=playthrough_name)

        # Act
        result = manager.get_characters_at_current_place_plus_followers()

        # Assert
        mock_get_characters_at_current_place.assert_called_once()
        mock_get_followers.assert_called_once()
        assert result == []
