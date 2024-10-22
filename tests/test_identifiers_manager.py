# Mocking the FilesystemManager since its implementation is not provided
from unittest.mock import MagicMock

import pytest

from src.base.enums import IdentifierType
from src.base.identifiers_manager import IdentifiersManager


class FilesystemManager:
    def get_file_path_to_playthrough_metadata(self, playthrough_name: str):
        pass

    def load_existing_or_new_json_file(self, path):
        pass


# Tests for the __init__ method
def test_init_with_filesystem_manager():
    playthrough_name = "test_playthrough"
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    assert identifiers_manager._playthrough_name == playthrough_name
    assert identifiers_manager._filesystem_manager == mock_filesystem_manager


# Tests for the get_highest_identifier static method
def test_get_highest_identifier():
    data = {"1": {}, "2": {}, "3": {}}
    result = IdentifiersManager.get_highest_identifier(data)
    assert result == "3"


def test_get_highest_identifier_with_negative_numbers():
    data = {"-5": {}, "-1": {}, "-10": {}}
    result = IdentifiersManager.get_highest_identifier(data)
    assert result == "-1"


def test_get_highest_identifier_with_non_integer_keys():
    data = {"a": {}, "2": {}, "3": {}}
    with pytest.raises(ValueError):
        IdentifiersManager.get_highest_identifier(data)


def test_get_highest_identifier_with_empty_dict():
    data = {}
    with pytest.raises(ValueError):
        IdentifiersManager.get_highest_identifier(data)


# Tests for the determine_next_identifier method
def test_determine_next_identifier_success():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.PLACES
    playthrough_metadata = {"last_identifiers": {"places": "5", "characters": "10"}}

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        playthrough_metadata
    )

    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    next_identifier = identifiers_manager.determine_next_identifier(identifier_type)
    assert next_identifier == 6
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.assert_called_once_with(
        playthrough_name
    )
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
        "/path/to/metadata.json"
    )


def test_determine_next_identifier_missing_identifier_type():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.PLACES
    playthrough_metadata = {"last_identifiers": {"characters": "10"}}

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        playthrough_metadata
    )

    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    with pytest.raises(KeyError):
        identifiers_manager.determine_next_identifier(identifier_type)


def test_determine_next_identifier_missing_last_identifiers():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.PLACES
    playthrough_metadata = {
        # "last_identifiers" is missing
    }

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        playthrough_metadata
    )

    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    with pytest.raises(KeyError):
        identifiers_manager.determine_next_identifier(identifier_type)


def test_determine_next_identifier_invalid_current_value():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.PLACES
    playthrough_metadata = {
        "last_identifiers": {"places": "invalid_number", "characters": "10"}
    }

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        playthrough_metadata
    )

    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    with pytest.raises(ValueError):
        identifiers_manager.determine_next_identifier(identifier_type)


def test_determine_next_identifier_characters():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS
    playthrough_metadata = {"last_identifiers": {"places": "5", "characters": "10"}}

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        playthrough_metadata
    )

    identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
    next_identifier = identifiers_manager.determine_next_identifier(identifier_type)
    assert next_identifier == 11
