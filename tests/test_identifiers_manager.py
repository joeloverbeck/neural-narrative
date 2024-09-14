from unittest.mock import Mock, patch

import pytest

from src.enums import IdentifierType
# Import the class and dependencies
from src.identifiers_manager import IdentifiersManager


def test_determine_next_identifier():
    # Arrange
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS

    # Create a mock for FilesystemManager
    mock_filesystem_manager = Mock()

    # Mock the methods called within IdentifiersManager
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = "/path/to/metadata.json"
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {
            identifier_type.value: 42
        }
    }

    # Mock logging configuration
    with patch('logging.config.dictConfig'):
        # Act
        identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
        next_id = identifiers_manager.determine_next_identifier(identifier_type)

    # Assert
    assert next_id == 43, "The next identifier should be incremented by 1."


def test_produce_and_update_next_identifier():
    # Arrange
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS

    # Create a mock for FilesystemManager
    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = "/path/to/metadata.json"
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {
            identifier_type.value: 42
        }
    }

    # Mock the StoreLastIdentifierCommand's execute method
    with patch('src.identifiers_manager.StoreLastIdentifierCommand') as mock_command_class:
        mock_command_instance = mock_command_class.return_value
        mock_command_instance.execute.return_value = None

        # Mock logging configuration
        with patch('logging.config.dictConfig'):
            # Act
            identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
            next_id = identifiers_manager.produce_and_update_next_identifier(identifier_type)

        # Assert
        assert next_id == 43, "The next identifier should be incremented by 1."
        mock_command_class.assert_called_once_with(playthrough_name, identifier_type, next_id)
        mock_command_instance.execute.assert_called_once()


def test_determine_next_identifier_key_error():
    # Arrange
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS

    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value = "/path/to/metadata.json"
    # Simulate missing identifier in the metadata
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {}
    }

    # Act & Assert
    with patch('logging.config.dictConfig'), pytest.raises(KeyError):
        identifiers_manager = IdentifiersManager(playthrough_name, mock_filesystem_manager)
        identifiers_manager.determine_next_identifier(identifier_type)
