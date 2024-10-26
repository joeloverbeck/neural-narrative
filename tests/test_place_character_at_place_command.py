from unittest.mock import Mock, patch

import pytest

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.movements.commands.place_character_at_place_command import (
    PlaceCharacterAtPlaceCommand,
)
# Assuming the following imports based on your provided code
from src.movements.exceptions import PlaceCharacterAtPlaceError


class TestPlaceCharacterAtPlaceCommand:

    def test_init_with_empty_playthrough_name_raises_exception(self):
        with pytest.raises(ValueError):
            PlaceCharacterAtPlaceCommand("", "test_character", "test_place")

    def test_init_with_empty_character_identifier_raises_exception(self):
        with pytest.raises(ValueError):
            PlaceCharacterAtPlaceCommand("test_playthrough", "", "test_place")

    def test_init_with_empty_place_identifier_raises_exception(self):
        with pytest.raises(ValueError):
            PlaceCharacterAtPlaceCommand("test_playthrough", "test_character", "")

    @patch("src.base.playthrough_manager.PlaythroughManager")
    @patch("src.filesystem.filesystem_manager.FilesystemManager")
    def test_execute_character_in_followers_raises_exception(
        self, mock_filesystem_manager_class, mock_playthrough_manager_class
    ):
        # Arrange
        playthrough_name = "test_playthrough"
        character_identifier = "test_character"
        place_identifier = "test_place"

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_playthrough_manager.get_followers.return_value = [character_identifier]
        mock_playthrough_manager_class.return_value = mock_playthrough_manager

        mock_filesystem_manager = Mock(spec=FilesystemManager)
        mock_filesystem_manager_class.return_value = mock_filesystem_manager

        command = PlaceCharacterAtPlaceCommand(
            playthrough_name,
            character_identifier,
            place_identifier,
            mock_playthrough_manager,
            mock_filesystem_manager,
        )

        # Act & Assert
        with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
            command.execute()
        assert f"Character {character_identifier} is one of the followers" in str(
            exc_info.value
        )

    @patch("src.movements.commands.place_character_at_place_command.read_json_file")
    @patch("src.filesystem.filesystem_manager.FilesystemManager")
    @patch("src.base.playthrough_manager.PlaythroughManager")
    def test_execute_place_not_found_raises_value_error(
        self,
        mock_filesystem_manager_class,
        mock_playthrough_manager_class,
        mock_read_json_file,
    ):
        # Arrange
        playthrough_name = "test_playthrough"
        character_identifier = "test_character"
        place_identifier = "nonexistent_place"

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_playthrough_manager.get_followers.return_value = []
        mock_playthrough_manager_class.return_value = mock_playthrough_manager

        mock_filesystem_manager = Mock(spec=FilesystemManager)
        mock_filesystem_manager.get_file_path_to_map.return_value = (
            "dummy_path.json"  # Set a valid path
        )
        mock_read_json_file.return_value = {}
        mock_filesystem_manager_class.return_value = mock_filesystem_manager

        command = PlaceCharacterAtPlaceCommand(
            playthrough_name,
            character_identifier,
            place_identifier,
            mock_playthrough_manager,
            mock_filesystem_manager,
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            command.execute()
        assert f"Place ID {place_identifier} not found." in str(exc_info.value)

    @patch("src.movements.commands.place_character_at_place_command.read_json_file")
    @patch("src.base.playthrough_manager.PlaythroughManager")
    @patch("src.filesystem.filesystem_manager.FilesystemManager")
    def test_execute_place_type_invalid_raises_exception(
        self,
        mock_filesystem_manager_class,
        mock_playthrough_manager_class,
        mock_read_json_file,
    ):
        # Arrange
        playthrough_name = "test_playthrough"
        character_identifier = "test_character"
        place_identifier = "test_place"

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_playthrough_manager.get_followers.return_value = []
        mock_playthrough_manager_class.return_value = mock_playthrough_manager

        map_file = {place_identifier: {"type": "invalid_type"}}
        mock_filesystem_manager = Mock(spec=FilesystemManager)
        mock_filesystem_manager.get_file_path_to_map.return_value = (
            "dummy_path.json"  # Set a valid path
        )
        mock_read_json_file.return_value = map_file
        mock_filesystem_manager_class.return_value = mock_filesystem_manager

        command = PlaceCharacterAtPlaceCommand(
            playthrough_name,
            character_identifier,
            place_identifier,
            mock_playthrough_manager,
            mock_filesystem_manager,
        )

        # Act & Assert
        with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
            command.execute()
        assert f"Place type 'invalid_type' cannot house characters." in str(
            exc_info.value
        )

    @patch("src.movements.commands.place_character_at_place_command.read_json_file")
    @patch("src.base.playthrough_manager.PlaythroughManager")
    @patch("src.filesystem.filesystem_manager.FilesystemManager")
    def test_execute_character_already_at_place_raises_exception(
        self,
        mock_filesystem_manager_class,
        mock_playthrough_manager_class,
        mock_read_json_file,
    ):
        # Arrange
        playthrough_name = "test_playthrough"
        character_identifier = "test_character"
        place_identifier = "test_place"

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_playthrough_manager.get_followers.return_value = []
        mock_playthrough_manager_class.return_value = mock_playthrough_manager

        map_file = {
            place_identifier: {"type": "area", "characters": [character_identifier]}
        }
        mock_filesystem_manager = Mock(spec=FilesystemManager)
        mock_read_json_file.return_value = map_file
        mock_filesystem_manager.get_file_path_to_map.return_value = (
            "dummy_path.json"  # Set a valid path
        )
        mock_filesystem_manager_class.return_value = mock_filesystem_manager

        command = PlaceCharacterAtPlaceCommand(
            playthrough_name,
            character_identifier,
            place_identifier,
            mock_playthrough_manager,
            mock_filesystem_manager,
        )

        # Act & Assert
        with pytest.raises(PlaceCharacterAtPlaceError) as exc_info:
            command.execute()
        assert (
            f"Character {character_identifier} is already at place {place_identifier}."
            in str(exc_info.value)
        )

    @patch("src.movements.commands.place_character_at_place_command.read_json_file")
    @patch("src.movements.commands.place_character_at_place_command.logger")
    @patch("src.base.playthrough_manager.PlaythroughManager")
    @patch("src.filesystem.filesystem_manager.FilesystemManager")
    def test_execute_character_placed_successfully(
        self,
        mock_filesystem_manager_class,
        mock_playthrough_manager_class,
        mock_logger,
        mock_read_json_file,
    ):
        # Arrange
        playthrough_name = "test_playthrough"
        character_identifier = "new_character"
        place_identifier = "test_place"

        mock_playthrough_manager = Mock(spec=PlaythroughManager)
        mock_playthrough_manager.get_followers.return_value = []
        mock_playthrough_manager_class.return_value = mock_playthrough_manager

        map_file = {place_identifier: {"type": "area", "characters": []}}
        mock_filesystem_manager = Mock(spec=FilesystemManager)
        mock_read_json_file.return_value = map_file
        mock_filesystem_manager.get_file_path_to_map.return_value = (
            "dummy_path.json"  # Set a valid path
        )
        mock_filesystem_manager_class.return_value = mock_filesystem_manager

        command = PlaceCharacterAtPlaceCommand(
            playthrough_name,
            character_identifier,
            place_identifier,
            mock_playthrough_manager,
            mock_filesystem_manager,
        )

        # Act
        command.execute()

        # Assert
        assert character_identifier in map_file[place_identifier]["characters"]
        mock_filesystem_manager.save_json_file.assert_called_once()
        mock_logger.info.assert_called_once_with(
            f"Character '{character_identifier}' placed at area '{place_identifier}'. Current character list: {map_file[place_identifier]['characters']}"
        )
