# test_characters_manager.py

from unittest.mock import Mock, patch

import pytest

from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager


def test_init_with_valid_playthrough_name():
    playthrough_name = "test_playthrough"
    manager = CharactersManager(playthrough_name)
    assert manager._playthrough_name == playthrough_name
    assert isinstance(manager._filesystem_manager, FilesystemManager)
    assert isinstance(manager._identifiers_manager, IdentifiersManager)
    assert isinstance(manager._playthrough_manager, PlaythroughManager)


def test_init_with_empty_playthrough_name():
    with pytest.raises(ValueError) as excinfo:
        CharactersManager("")
    assert "playthrough_name should not be empty." in str(excinfo.value)


def test_get_latest_character_identifier():
    playthrough_name = "test_playthrough"
    mock_filesystem_manager = Mock()
    mock_identifiers_manager = Mock()
    mock_characters_file = {"char1": {}, "char2": {}}
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        mock_characters_file
    )
    mock_identifiers_manager.get_highest_identifier.return_value = "char2"

    manager = CharactersManager(
        playthrough_name,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    latest_id = manager.get_latest_character_identifier()
    assert latest_id == "char2"
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once()
    mock_identifiers_manager.get_highest_identifier.assert_called_with(
        mock_characters_file
    )


def test_get_characters():
    playthrough_name = "test_playthrough"
    character_identifiers = ["char1", "char2"]
    with patch("src.characters.characters_manager.Character") as MockCharacter:
        manager = CharactersManager(playthrough_name)
        characters = manager.get_characters(character_identifiers)
        assert len(characters) == 2
        MockCharacter.assert_any_call(playthrough_name, "char1")
        MockCharacter.assert_any_call(playthrough_name, "char2")


def test_get_followers():
    playthrough_name = "test_playthrough"
    mock_playthrough_manager = Mock()
    mock_playthrough_manager.get_followers.return_value = ["char1", "char3"]
    with patch.object(
        CharactersManager, "get_characters", return_value=["Character1", "Character3"]
    ) as mock_get_characters:
        manager = CharactersManager(
            playthrough_name, playthrough_manager=mock_playthrough_manager
        )
        followers = manager.get_followers()
        assert followers == ["Character1", "Character3"]
        mock_playthrough_manager.get_followers.assert_called_once()
        mock_get_characters.assert_called_with(["char1", "char3"])


def test_get_characters_at_current_place():
    playthrough_name = "test_playthrough"
    mock_playthrough_manager = Mock()
    mock_playthrough_manager.get_current_place_identifier.return_value = "place1"
    mock_filesystem_manager = Mock()
    mock_map_file = {
        "place1": {"characters": ["char2", "char4"]},
        "place2": {"characters": ["char5"]},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = mock_map_file
    with patch.object(
        CharactersManager, "get_characters", return_value=["Character2", "Character4"]
    ) as mock_get_characters:
        manager = CharactersManager(
            playthrough_name,
            filesystem_manager=mock_filesystem_manager,
            playthrough_manager=mock_playthrough_manager,
        )
        characters = manager.get_characters_at_current_place()
        assert characters == ["Character2", "Character4"]
        mock_playthrough_manager.get_current_place_identifier.assert_called_once()
        mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once()
        mock_get_characters.assert_called_with(["char2", "char4"])


def test_get_characters_at_current_place_plus_followers():
    playthrough_name = "test_playthrough"
    with patch.object(
        CharactersManager,
        "get_characters_at_current_place",
        return_value=["CharAtPlace1", "CharAtPlace2"],
    ) as mock_get_characters_at_place:
        with patch.object(
            CharactersManager, "get_followers", return_value=["Follower1"]
        ) as mock_get_followers:
            manager = CharactersManager(playthrough_name)
            characters = manager.get_characters_at_current_place_plus_followers()
            assert characters == ["CharAtPlace1", "CharAtPlace2", "Follower1"]
            mock_get_characters_at_place.assert_called_once()
            mock_get_followers.assert_called_once()


def test_get_all_characters():
    playthrough_name = "test_playthrough"
    mock_filesystem_manager = Mock()
    mock_characters_file = {
        "char1": {"name": "Alice"},
        "char2": {"name": "Bob"},
        "char3": {},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        mock_characters_file
    )
    manager = CharactersManager(
        playthrough_name, filesystem_manager=mock_filesystem_manager
    )
    all_characters = manager.get_all_characters()
    expected_characters = [
        {"identifier": "char1", "name": "Alice"},
        {"identifier": "char2", "name": "Bob"},
        {"identifier": "char3", "name": "Unknown"},
    ]
    assert all_characters == expected_characters
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once()


def test_get_all_character_names():
    playthrough_name = "test_playthrough"
    mock_filesystem_manager = Mock()
    mock_characters_file = {
        "char1": {"name": "Alice"},
        "char2": {"name": "Bob"},
        "char3": {},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        mock_characters_file
    )
    manager = CharactersManager(
        playthrough_name, filesystem_manager=mock_filesystem_manager
    )
    all_names = manager.get_all_character_names()
    expected_names = ["Alice", "Bob", ""]
    assert all_names == expected_names
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once()
