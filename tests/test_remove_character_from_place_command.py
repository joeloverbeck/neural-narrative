from unittest.mock import Mock, patch

import pytest

from src.maps.commands.remove_character_from_place_command import (
    RemoveCharacterFromPlaceCommand,
)
# Assuming the module path is as provided in the original code
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


# Test Initialization


def test_remove_character_from_place_command_initialization_with_map_repository():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    map_repository = Mock(spec=MapRepository)

    # Act
    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Assert
    assert command._character_identifier == character_identifier
    assert command._place_identifier == place_identifier
    assert command._place_manager_factory is place_manager_factory
    assert command._map_repository is map_repository


def test_remove_character_from_place_command_initialization_without_map_repository():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)

    with patch(
        "src.maps.commands.remove_character_from_place_command.MapRepository"
    ) as MockMapRepository:
        mock_map_repository_instance = MockMapRepository.return_value

        # Act
        command = RemoveCharacterFromPlaceCommand(
            playthrough_name=playthrough_name,
            character_identifier=character_identifier,
            place_identifier=place_identifier,
            place_manager_factory=place_manager_factory,
            map_repository=None,
        )

        # Assert
        MockMapRepository.assert_called_once_with(playthrough_name)
        assert command._map_repository is mock_map_repository_instance


@pytest.mark.parametrize(
    "character_identifier, place_identifier",
    [
        ("", "valid_place"),
        ("valid_char", ""),
        ("", ""),
    ],
)
def test_remove_character_from_place_command_initialization_invalid_strings(
    character_identifier, place_identifier
):
    # Arrange
    playthrough_name = "TestPlaythrough"
    place_manager_factory = Mock(spec=PlaceManagerFactory)

    with pytest.raises(ValueError) as exc_info:
        # Assuming validate_non_empty_string raises ValueError for empty strings
        RemoveCharacterFromPlaceCommand(
            playthrough_name=playthrough_name,
            character_identifier=character_identifier,
            place_identifier=place_identifier,
            place_manager_factory=place_manager_factory,
        )

    assert "non-empty" in str(exc_info.value).lower()


# Test Execute Method


def test_remove_character_from_place_command_execute_removes_character():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {"characters": ["char_123", "char_789", "char_456"]}
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {
        place_identifier: initial_place.copy(),
        "other_place": {},
    }

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act
    command.execute()

    # Assert
    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)

    # Check that character was removed
    expected_place = initial_place.copy()
    expected_place["characters"] = ["char_789", "char_456"]
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_called_once_with(
        {place_identifier: expected_place, "other_place": {}}
    )


def test_remove_character_from_place_command_execute_character_not_in_place():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_nonexistent"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {"characters": ["char_789", "char_456"]}
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {
        place_identifier: initial_place.copy(),
        "other_place": {},
    }

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act
    command.execute()

    # Assert
    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)

    # Check that map data remains unchanged
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_called_once_with(
        {place_identifier: initial_place, "other_place": {}}
    )


def test_remove_character_from_place_command_execute_no_characters_in_place():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_empty"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {"characters": []}
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {
        place_identifier: initial_place.copy(),
        "other_place": {},
    }

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act
    command.execute()

    # Assert
    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)

    # Check that map data remains unchanged
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_called_once_with(
        {place_identifier: initial_place, "other_place": {}}
    )


def test_remove_character_from_place_command_execute_place_does_not_exist():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "nonexistent_place"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    place_manager.get_place.side_effect = KeyError("Place not found")

    map_repository = Mock(spec=MapRepository)

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act & Assert
    with pytest.raises(KeyError, match="Place not found"):
        command.execute()

    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)
    map_repository.load_map_data.assert_not_called()
    map_repository.save_map_data.assert_not_called()


def test_remove_character_from_place_command_execute_map_repository_load_failure():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {"characters": ["char_123", "char_789"]}
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.side_effect = IOError("Failed to load map data")

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act & Assert
    with pytest.raises(IOError, match="Failed to load map data"):
        command.execute()

    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_not_called()


def test_remove_character_from_place_command_execute_map_repository_save_failure():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_456"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {"characters": ["char_123", "char_789"]}
    updated_place = {"characters": ["char_789"]}
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {place_identifier: initial_place.copy()}
    map_repository.save_map_data.side_effect = IOError("Failed to save map data")

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act & Assert
    with pytest.raises(IOError, match="Failed to save map data"):
        command.execute()

    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_called_once_with(
        {place_identifier: updated_place}
    )


def test_remove_character_from_place_command_execute_no_characters_key():
    # Arrange
    playthrough_name = "TestPlaythrough"
    character_identifier = "char_123"
    place_identifier = "place_no_characters"
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    initial_place = {
        # No 'characters' key
    }
    place_manager.get_place.return_value = initial_place.copy()

    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {place_identifier: initial_place.copy()}

    command = RemoveCharacterFromPlaceCommand(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        place_identifier=place_identifier,
        place_manager_factory=place_manager_factory,
        map_repository=map_repository,
    )

    # Act
    command.execute()

    # Assert
    place_manager_factory.create_place_manager.assert_called_once()
    place_manager.get_place.assert_called_once_with(place_identifier)

    # 'characters' key should default to empty list
    map_repository.load_map_data.assert_called_once()
    map_repository.save_map_data.assert_called_once_with(
        {place_identifier: {"characters": []}}
    )
