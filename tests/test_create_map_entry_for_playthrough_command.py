from unittest.mock import Mock
import pytest
from src.base.enums import TemplateType, IdentifierType
from src.base.identifiers_manager import IdentifiersManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)


def test_execute_creates_map_entry_successfully():
    playthrough_name = "TestPlaythrough"
    father_identifier = "FatherID1"
    place_type = TemplateType.LOCATION
    place_template = "TestLocationTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    (mock_identifiers_manager.produce_and_update_next_identifier.return_value) = 1
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    command.execute()
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
        "path/to/map.json"
    )
    mock_identifiers_manager.produce_and_update_next_identifier.assert_called_once_with(
        IdentifierType.PLACES
    )
    expected_map_entry = {
        "type": place_type,
        "place_template": place_template,
        "area": father_identifier,
        "characters": [],
        "visited": False,
    }
    expected_map_file = {"1": expected_map_entry}
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_raises_value_error_when_father_identifier_missing():
    playthrough_name = "TestPlaythrough"
    father_identifier = None
    place_type = TemplateType.LOCATION
    place_template = "TestLocationTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    with pytest.raises(ValueError) as excinfo:
        command.execute()
    assert (
        f"When creating a map entry for '{place_type}', the father's identifier is required but was not provided."
        in str(excinfo)
    )


def test_execute_without_father_identifier_for_world():
    playthrough_name = "TestPlaythrough"
    father_identifier = None
    place_type = TemplateType.WORLD
    place_template = "TestWorldTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    (mock_identifiers_manager.produce_and_update_next_identifier.return_value) = 1
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    command.execute()
    expected_map_entry = {"type": place_type, "place_template": place_template}
    expected_map_file = {"1": expected_map_entry}
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_with_area_type_adds_additional_fields():
    playthrough_name = "TestPlaythrough"
    father_identifier = "FatherID1"
    place_type = TemplateType.AREA
    place_template = "TestAreaTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    (mock_identifiers_manager.produce_and_update_next_identifier.return_value) = 1
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    command.execute()
    expected_map_entry = {
        "type": place_type,
        "place_template": place_template,
        "region": father_identifier,
        "weather_identifier": "sunny",
        "locations": [],
        "characters": [],
        "visited": False,
    }
    expected_map_file = {"1": expected_map_entry}
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_adds_entry_to_existing_map_file():
    playthrough_name = "TestPlaythrough"
    father_identifier = "FatherID1"
    place_type = TemplateType.LOCATION
    place_template = "TestLocationTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    existing_map_file = {
        "1": {
            "type": "location",
            "place_template": "ExistingLocation",
            "area": "FatherID1",
            "characters": [],
            "visited": False,
        }
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        existing_map_file
    )
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    (mock_identifiers_manager.produce_and_update_next_identifier.return_value) = 2
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    command.execute()
    new_map_entry = {
        "type": place_type,
        "place_template": place_template,
        "area": father_identifier,
        "characters": [],
        "visited": False,
    }
    expected_map_file = existing_map_file.copy()
    expected_map_file["2"] = new_map_entry
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_handles_exception_on_save():
    playthrough_name = "TestPlaythrough"
    father_identifier = "FatherID1"
    place_type = TemplateType.LOCATION
    place_template = "TestLocationTemplate"
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    mock_filesystem_manager.save_json_file.side_effect = Exception(
        "Failed to save file"
    )
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    (mock_identifiers_manager.produce_and_update_next_identifier.return_value) = 1
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )
    with pytest.raises(Exception) as excinfo:
        command.execute()
    assert "Failed to save file" in str(excinfo)
