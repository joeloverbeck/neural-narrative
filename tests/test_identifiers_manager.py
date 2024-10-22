from unittest.mock import Mock, patch
import pytest
from src.base.enums import IdentifierType
from src.base.identifiers_manager import IdentifiersManager


def test_determine_next_identifier():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS
    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    (mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {identifier_type: 42}
    }
    with patch("logging.config.dictConfig"):
        identifiers_manager = IdentifiersManager(
            playthrough_name, mock_filesystem_manager
        )
        next_id = identifiers_manager.determine_next_identifier(identifier_type)
    assert next_id == 43, "The next identifier should be incremented by 1."


def test_produce_and_update_next_identifier():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS
    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    (mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {identifier_type: 42}
    }
    with patch(
        "src.base.identifiers_manager.StoreLastIdentifierCommand"
    ) as mock_command_class:
        mock_command_instance = mock_command_class.return_value
        mock_command_instance.execute.return_value = None
        with patch("logging.config.dictConfig"):
            identifiers_manager = IdentifiersManager(
                playthrough_name, mock_filesystem_manager
            )
            next_id = identifiers_manager.produce_and_update_next_identifier(
                identifier_type
            )
        assert next_id == 43, "The next identifier should be incremented by 1."
        mock_command_class.assert_called_once_with(
            playthrough_name, identifier_type, next_id
        )
        mock_command_instance.execute.assert_called_once()


def test_determine_next_identifier_key_error():
    playthrough_name = "test_playthrough"
    identifier_type = IdentifierType.CHARACTERS
    mock_filesystem_manager = Mock()
    mock_filesystem_manager.get_logging_config_file.return_value = {}
    (mock_filesystem_manager.get_file_path_to_playthrough_metadata.return_value) = (
        "/path/to/metadata.json"
    )
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "last_identifiers": {}
    }
    with patch("logging.config.dictConfig"), pytest.raises(KeyError):
        identifiers_manager = IdentifiersManager(
            playthrough_name, mock_filesystem_manager
        )
        identifiers_manager.determine_next_identifier(identifier_type)
