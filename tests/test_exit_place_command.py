from unittest.mock import Mock, patch

import pytest

from src.base.constants import PARENT_KEYS
from src.base.enums import TemplateType
from src.movements.commands.exit_place_command import ExitPlaceCommand


def test_exit_place_command_from_location():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create mocks
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    map_repository = Mock()
    path_manager = Mock()

    # Create the command
    command = ExitPlaceCommand(
        playthrough_name,
        visit_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        map_repository,
        path_manager,
    )

    # Mock the place_manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager_factory.create_place_manager.return_value = place_manager

    # Mock the playthrough_manager
    current_place_identifier = "location_1"
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    # Mock the map_repository
    map_data = {
        current_place_identifier: {PARENT_KEYS[TemplateType.LOCATION]: "area_1"}
    }
    map_repository.load_map_data.return_value = map_data

    # Mock the visit_place_command
    visit_place_command = Mock()
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )

    # Act
    command.execute()

    # Assert
    # Ensure that the destination area is 'area_1'
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        "area_1"
    )
    visit_place_command.execute.assert_called_once()


def test_exit_place_command_from_room():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create mocks
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    map_repository = Mock()
    path_manager = Mock()

    # Create the command
    command = ExitPlaceCommand(
        playthrough_name,
        visit_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        map_repository,
        path_manager,
    )

    # Mock the place_manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.ROOM
    place_manager_factory.create_place_manager.return_value = place_manager

    # Mock the playthrough_manager
    current_place_identifier = "room_1"
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    # Mock the map_repository
    map_data = {
        current_place_identifier: {PARENT_KEYS[TemplateType.ROOM]: "location_1"}
    }
    map_repository.load_map_data.return_value = map_data

    # Mock the visit_place_command
    visit_place_command = Mock()
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )

    # Act
    command.execute()

    # Assert
    # Ensure that the destination location is 'location_1'
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        "location_1"
    )
    visit_place_command.execute.assert_called_once()


def test_exit_place_command_invalid_place_type():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create mocks
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    map_repository = Mock()
    path_manager = Mock()

    # Create the command
    command = ExitPlaceCommand(
        playthrough_name,
        visit_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        map_repository,
        path_manager,
    )

    # Mock the place_manager to return an invalid place type
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.AREA
    place_manager_factory.create_place_manager.return_value = place_manager

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert (
        "Somehow tried to exit a location when the current place wasn't a location nor a room."
        in str(exc_info.value)
    )


def test_exit_place_command_missing_map_data():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create mocks
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    map_repository = Mock()
    path_manager = Mock()

    # Create the command
    command = ExitPlaceCommand(
        playthrough_name,
        visit_place_command_factory,
        place_manager_factory,
        playthrough_manager,
        map_repository,
        path_manager,
    )

    # Mock the place_manager
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    place_manager_factory.create_place_manager.return_value = place_manager

    # Mock the playthrough_manager
    current_place_identifier = "location_1"
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    # Mock the map_repository with missing map data
    map_data = {}  # Empty map data
    map_repository.load_map_data.return_value = map_data

    # Act & Assert
    with pytest.raises(KeyError):
        command.execute()


def test_exit_place_command_defaults():
    # Arrange
    playthrough_name = "test_playthrough"
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()

    # No optional parameters provided
    with patch(
        "src.movements.commands.exit_place_command.PlaythroughManager"
    ) as MockPlaythroughManager, patch(
        "src.movements.commands.exit_place_command.MapRepository"
    ) as MockMapRepository, patch(
        "src.movements.commands.exit_place_command.PathManager"
    ) as MockPathManager:

        # Act
        ExitPlaceCommand(
            playthrough_name,
            visit_place_command_factory,
            place_manager_factory,
            # optional parameters not provided
        )

        # Assert
        MockPlaythroughManager.assert_called_once_with(playthrough_name)
        MockMapRepository.assert_called_once_with(playthrough_name)
        MockPathManager.assert_called_once()


def test_exit_place_command_with_provided_optional_parameters():
    # Arrange
    playthrough_name = "test_playthrough"
    visit_place_command_factory = Mock()
    place_manager_factory = Mock()
    playthrough_manager = Mock()
    map_repository = Mock()
    path_manager = Mock()

    with patch(
        "src.base.playthrough_manager.PlaythroughManager"
    ) as MockPlaythroughManager, patch(
        "src.maps.map_repository.MapRepository"
    ) as MockMapRepository, patch(
        "src.filesystem.path_manager.PathManager"
    ) as MockPathManager:

        # Act
        ExitPlaceCommand(
            playthrough_name,
            visit_place_command_factory,
            place_manager_factory,
            playthrough_manager,
            map_repository,
            path_manager,
        )

        # Assert that default instances were not created
        MockPlaythroughManager.assert_not_called()
        MockMapRepository.assert_not_called()
        MockPathManager.assert_not_called()
