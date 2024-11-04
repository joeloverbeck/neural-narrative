from unittest.mock import Mock

import pytest

from src.base.constants import CHILDREN_KEYS
from src.base.enums import TemplateType
from src.maps.commands.attach_place_command import AttachPlaceCommand


def test_init_with_valid_inputs():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "test_map_entry"
    place_manager = Mock()

    # Act
    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
    )

    # Assert
    assert command._map_entry_identifier == map_entry_identifier
    assert command._place_manager == place_manager
    assert command._playthrough_manager is not None
    assert command._map_repository is not None
    assert command._time_manager is not None
    assert command._config_loader is not None


def test_init_with_empty_playthrough_name():
    # Arrange
    playthrough_name = ""
    map_entry_identifier = "test_map_entry"
    place_manager = Mock()

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        AttachPlaceCommand(
            playthrough_name=playthrough_name,
            map_entry_identifier=map_entry_identifier,
            place_manager=place_manager,
        )
    assert "'playthrough_name' must be" in str(exc_info.value)


def test_init_with_empty_map_entry_identifier():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = ""
    place_manager = Mock()

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        AttachPlaceCommand(
            playthrough_name=playthrough_name,
            map_entry_identifier=map_entry_identifier,
            place_manager=place_manager,
        )
    assert "'map_entry_identifier' must be" in str(exc_info.value)


def test_execute_with_invalid_current_place_type():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "test_map_entry"
    invalid_place_type = TemplateType.WORLD
    place_manager = Mock()
    place_manager.get_current_place_type.return_value = invalid_place_type

    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
    )

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    expected_message = (
        f"Attempted to attach a place to the current place type, "
        f"that is neither an area nor a location: '{invalid_place_type}'."
    )
    assert expected_message in str(exc_info.value)


def test_execute_when_map_entry_identifier_already_present():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "existing_entry"
    current_place_type = TemplateType.AREA
    children_key = CHILDREN_KEYS[current_place_type]
    current_place_identifier = "current_place"

    place_manager = Mock()
    place_manager.get_current_place_type.return_value = current_place_type

    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    map_file = {current_place_identifier: {children_key: [map_entry_identifier]}}
    map_repository = Mock()
    map_repository.load_map_data.return_value = map_file

    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
        playthrough_manager=playthrough_manager,
        map_repository=map_repository,
    )

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    expected_message = (
        f"Map entry identifier '{map_entry_identifier}' already present in the "
        f"{children_key} of the current {current_place_type}."
    )
    assert expected_message in str(exc_info.value)


def test_execute_successful_attachment():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "new_entry"
    current_place_type = TemplateType.AREA
    children_key = CHILDREN_KEYS[current_place_type]
    current_place_identifier = "current_place"

    place_manager = Mock()
    place_manager.get_current_place_type.return_value = current_place_type

    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    map_file = {current_place_identifier: {children_key: []}}
    map_repository = Mock()
    map_repository.load_map_data.return_value = map_file

    time_manager = Mock()
    config_loader = Mock()
    config_loader.get_time_advanced_due_to_searching_for_location.return_value = 5

    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
        playthrough_manager=playthrough_manager,
        map_repository=map_repository,
        time_manager=time_manager,
        config_loader=config_loader,
    )

    # Act
    command.execute()

    # Assert
    assert map_entry_identifier in map_file[current_place_identifier][children_key]
    map_repository.save_map_data.assert_called_once_with(map_file)
    time_manager.advance_time.assert_called_once_with(5)


def test_execute_with_location_place_type():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "new_room"
    current_place_type = TemplateType.LOCATION
    children_key = CHILDREN_KEYS[current_place_type]
    current_place_identifier = "current_location"

    place_manager = Mock()
    place_manager.get_current_place_type.return_value = current_place_type

    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    map_file = {current_place_identifier: {children_key: []}}
    map_repository = Mock()
    map_repository.load_map_data.return_value = map_file

    time_manager = Mock()
    config_loader = Mock()
    config_loader.get_time_advanced_due_to_searching_for_location.return_value = 10

    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
        playthrough_manager=playthrough_manager,
        map_repository=map_repository,
        time_manager=time_manager,
        config_loader=config_loader,
    )

    # Act
    command.execute()

    # Assert
    assert map_entry_identifier in map_file[current_place_identifier][children_key]
    map_repository.save_map_data.assert_called_once_with(map_file)
    time_manager.advance_time.assert_called_once_with(10)


def test_time_advanced_correctly():
    # Arrange
    playthrough_name = "test_playthrough"
    map_entry_identifier = "new_entry"
    current_place_type = TemplateType.AREA
    children_key = CHILDREN_KEYS[current_place_type]
    current_place_identifier = "current_place"

    place_manager = Mock()
    place_manager.get_current_place_type.return_value = current_place_type

    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    map_file = {current_place_identifier: {children_key: []}}
    map_repository = Mock()
    map_repository.load_map_data.return_value = map_file

    time_manager = Mock()
    config_loader = Mock()
    time_advanced_value = 7
    config_loader.get_time_advanced_due_to_searching_for_location.return_value = (
        time_advanced_value
    )

    command = AttachPlaceCommand(
        playthrough_name=playthrough_name,
        map_entry_identifier=map_entry_identifier,
        place_manager=place_manager,
        playthrough_manager=playthrough_manager,
        map_repository=map_repository,
        time_manager=time_manager,
        config_loader=config_loader,
    )

    # Act
    command.execute()

    # Assert
    time_manager.advance_time.assert_called_once_with(time_advanced_value)
