from unittest.mock import Mock

import pytest

from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import TemplateType
from src.base.identifiers_manager import IdentifiersManager
from src.filesystem.path_manager import PathManager
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)
from src.maps.map_repository import MapRepository


def test_create_map_entry_valid_location():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.LOCATION
    place_template = "location_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_456"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    expected_map_entry = {
        "type": "location",
        "place_template": "location_template",
        "area": "parent123",
        "characters": [],
        "rooms": [],
        "visited": False,
    }
    expected_map_file = {"new_id_456": expected_map_entry}
    map_repository.save_map_data.assert_called_once_with(expected_map_file)
    produce_and_update_next_identifier.do_algorithm.assert_called_once()


def test_create_map_entry_missing_father_identifier():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = None
    place_type = TemplateType.LOCATION
    place_template = "location_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    path_manager = Mock(spec=PathManager)

    # Act & Assert
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "the father's identifier is required but was not provided" in str(
        exc_info.value
    )


def test_create_map_entry_valid_area():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.AREA
    place_template = "area_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_789"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    expected_map_entry = {
        "type": "area",
        "place_template": "area_template",
        "region": "parent123",
        "weather_identifier": "sunny",
        "locations": [],
        "characters": [],
        "visited": False,
    }
    expected_map_file = {"new_id_789": expected_map_entry}
    map_repository.save_map_data.assert_called_once_with(expected_map_file)


def test_create_map_entry_no_parent_key():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = None
    place_type = TemplateType.WORLD
    place_template = "world_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_101"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    expected_map_entry = {"type": "world", "place_template": "world_template"}
    expected_map_file = {"new_id_101": expected_map_entry}
    map_repository.save_map_data.assert_called_once_with(expected_map_file)


def test_create_map_entry_with_empty_playthrough_name():
    # Arrange
    playthrough_name = ""
    father_identifier = "parent123"
    place_type = TemplateType.LOCATION
    place_template = "location_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    path_manager = Mock(spec=PathManager)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        CreateMapEntryForPlaythroughCommand(
            playthrough_name,
            father_identifier,
            place_type,
            place_template,
            produce_and_update_next_identifier,
            identifiers_manager,
            map_repository,
            path_manager,
        )
    assert "playthrough_name" in str(exc_info.value)


def test_create_map_entry_with_empty_place_template():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.LOCATION
    place_template = ""

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    path_manager = Mock(spec=PathManager)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        CreateMapEntryForPlaythroughCommand(
            playthrough_name,
            father_identifier,
            place_type,
            place_template,
            produce_and_update_next_identifier,
            identifiers_manager,
            map_repository,
            path_manager,
        )
    assert "place_template" in str(exc_info.value)


def test_create_map_entry_additional_fields_room():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.ROOM
    place_template = "room_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_202"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    expected_map_entry = {
        "type": "room",
        "place_template": "room_template",
        "location": "parent123",
        "characters": [],
    }
    expected_map_file = {"new_id_202": expected_map_entry}
    map_repository.save_map_data.assert_called_once_with(expected_map_file)


def test_create_map_entry_load_map_data_returns_none():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.LOCATION
    place_template = "location_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_303"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = None
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    expected_map_entry = {
        "type": "location",
        "place_template": "location_template",
        "area": "parent123",
        "characters": [],
        "rooms": [],
        "visited": False,
    }
    expected_map_file = {"new_id_303": expected_map_entry}
    map_repository.save_map_data.assert_called_once_with(expected_map_file)


def test_create_map_entry_invalid_place_type():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = "invalid_type"  # Not a valid TemplateType
    place_template = "template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    path_manager = Mock(spec=PathManager)

    # Act & Assert
    with pytest.raises(TypeError):
        CreateMapEntryForPlaythroughCommand(
            playthrough_name,
            father_identifier,
            place_type,  # noqa
            place_template,
            produce_and_update_next_identifier,
            identifiers_manager,
            map_repository,
            path_manager,
        )


def test_create_map_entry_produce_identifier_called():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.AREA
    place_template = "area_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_404"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    produce_and_update_next_identifier.do_algorithm.assert_called_once()


def test_create_map_entry_save_map_data_called_once():
    # Arrange
    playthrough_name = "test_playthrough"
    father_identifier = "parent123"
    place_type = TemplateType.ROOM
    place_template = "room_template"

    produce_and_update_next_identifier = Mock(
        spec=ProduceAndUpdateNextIdentifierAlgorithm
    )
    produce_and_update_next_identifier.do_algorithm.return_value = "new_id_505"

    identifiers_manager = Mock(spec=IdentifiersManager)
    map_repository = Mock(spec=MapRepository)
    map_repository.load_map_data.return_value = {"existing_id": {}}
    path_manager = Mock(spec=PathManager)

    # Act
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name,
        father_identifier,
        place_type,
        place_template,
        produce_and_update_next_identifier,
        identifiers_manager,
        map_repository,
        path_manager,
    )
    command.execute()

    # Assert
    map_repository.save_map_data.assert_called_once()
