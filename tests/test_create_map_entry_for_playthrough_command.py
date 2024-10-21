from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType, IdentifierType
from src.base.identifiers_manager import IdentifiersManager
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)


def test_execute_creates_map_entry_successfully():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = RequiredString("FatherID1")
    place_type = TemplateType.LOCATION
    place_template = RequiredString("TestLocationTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    # Configure mock to simulate loading an existing map file
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    # Configure mock for get_file_path_to_map
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    # Configure mock to produce a specific new identifier
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = 1

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command
    command.execute()

    # Assert that the map file was loaded
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_once_with(
        "path/to/map.json"
    )

    # Assert that a new identifier was produced
    mock_identifiers_manager.produce_and_update_next_identifier.assert_called_once_with(
        IdentifierType.PLACES
    )

    # Build expected map entry
    expected_map_entry = {
        "type": place_type.value,
        "place_template": place_template.value,
        "area": father_identifier.value,  # Since parent_key for LOCATION is 'area'
        "characters": [],
        "visited": False,
    }

    # The map file should be updated with new entry
    expected_map_file = {"1": expected_map_entry}

    # Assert that save_json_file was called with the expected data
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_raises_value_error_when_father_identifier_missing():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = None  # Not provided
    place_type = TemplateType.LOCATION  # Requires father identifier
    place_template = RequiredString("TestLocationTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command and expect ValueError
    with pytest.raises(ValueError) as excinfo:
        command.execute()

    # Check that the error message is as expected
    assert (
        f"When creating a map entry for '{place_type.value}', the father's identifier is required but was not provided."
        in str(excinfo.value)
    )


def test_execute_without_father_identifier_for_world():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = None  # Not provided
    place_type = TemplateType.WORLD  # Does not require father identifier
    place_template = RequiredString("TestWorldTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    # Assume empty map file
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = 1

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command
    command.execute()

    # Build expected map entry
    expected_map_entry = {
        "type": place_type.value,
        "place_template": place_template.value,
        # No parent key, no additional fields
    }

    # The map file should be updated with new entry
    expected_map_file = {"1": expected_map_entry}

    # Assert that save_json_file was called with the expected data
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_with_area_type_adds_additional_fields():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = RequiredString("FatherID1")
    place_type = TemplateType.AREA
    place_template = RequiredString("TestAreaTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    # Assume existing map file is empty dict
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = 1

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command
    command.execute()

    # Build expected map entry
    expected_map_entry = {
        "type": place_type.value,
        "place_template": place_template.value,
        "region": father_identifier.value,  # Parent key for AREA is 'region'
        "weather_identifier": "sunny",
        "locations": [],
        "characters": [],
        "visited": False,
    }

    # The map file should be updated with new entry
    expected_map_file = {"1": expected_map_entry}

    # Assert that save_json_file was called with the expected data
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_adds_entry_to_existing_map_file():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = RequiredString("FatherID1")
    place_type = TemplateType.LOCATION
    place_template = RequiredString("TestLocationTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    # Existing map file with one entry
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

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    # Let's assume that the next identifier is '2'
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = 2

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command
    command.execute()

    # Build expected map entry
    new_map_entry = {
        "type": place_type.value,
        "place_template": place_template.value,
        "area": father_identifier.value,
        "characters": [],
        "visited": False,
    }

    # The map file should be updated with the new entry
    expected_map_file = existing_map_file.copy()
    expected_map_file["2"] = new_map_entry

    # Assert that save_json_file was called with the expected data
    mock_filesystem_manager.save_json_file.assert_called_once_with(
        expected_map_file, "path/to/map.json"
    )


def test_execute_handles_exception_on_save():
    # Prepare the test inputs
    playthrough_name = RequiredString("TestPlaythrough")
    father_identifier = RequiredString("FatherID1")
    place_type = TemplateType.LOCATION
    place_template = RequiredString("TestLocationTemplate")

    # Create mock FilesystemManager
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    # Configure mock to simulate loading an existing map file
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.get_file_path_to_map.return_value = "path/to/map.json"
    # Simulate an exception when saving the file
    mock_filesystem_manager.save_json_file.side_effect = Exception(
        "Failed to save file"
    )

    # Create mock IdentifiersManager
    mock_identifiers_manager = Mock(spec=IdentifiersManager)
    # Configure mock to produce a specific new identifier
    mock_identifiers_manager.produce_and_update_next_identifier.return_value = 1

    # Instantiate the object under test
    command = CreateMapEntryForPlaythroughCommand(
        playthrough_name=playthrough_name,
        father_identifier=father_identifier,
        place_type=place_type,
        place_template=place_template,
        filesystem_manager=mock_filesystem_manager,
        identifiers_manager=mock_identifiers_manager,
    )

    # Execute the command and expect an exception
    with pytest.raises(Exception) as excinfo:
        command.execute()

    # Check that the exception message is as expected
    assert "Failed to save file" in str(excinfo.value)
