# Mock FilesystemManager
import logging
from typing import cast

import pytest

from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.maps.place_data import PlaceData


class MockFilesystemManager:
    def __init__(self):
        self.files = {}

    def load_existing_or_new_json_file(self, filename: RequiredString):
        if filename is None:
            raise ValueError("Filename cannot be None")
        return self.files.get(filename.value, {})

    def save_json_file(self, data, filename: RequiredString):
        if filename is None:
            raise ValueError("Filename cannot be None")
        self.files[filename.value] = data


# Pytest tests
def test_store_generated_place_command_normal_case():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[RequiredString("Category1"), RequiredString("Category2")],
        type=None,
    )
    template_type = TemplateType.REGION
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    command.execute()

    # Verify
    expected_data = {
        "TestPlace": {
            "description": "A test place",
            "categories": ["category1", "category2"],
        }
    }

    assert (
        filesystem_manager.files[TEMPLATE_FILES[template_type].value] == expected_data
    )


def test_store_generated_place_command_categories_lowercase():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[RequiredString("Category1"), RequiredString("CATEGORY2")],
        type=None,
    )
    template_type = TemplateType.REGION
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    command.execute()

    # Verify
    saved_data = filesystem_manager.files[TEMPLATE_FILES[template_type].value]
    categories = saved_data["TestPlace"]["categories"]
    assert categories == ["category1", "category2"]


def test_store_generated_place_command_location_with_type():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestLocation"),
        description=RequiredString("A test location"),
        categories=[RequiredString("Category1"), RequiredString("Category2")],
        type=RequiredString("BAR"),
    )
    template_type = TemplateType.LOCATION
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    command.execute()

    # Verify
    expected_data = {
        "TestLocation": {
            "description": "A test location",
            "categories": ["category1", "category2"],
            "type": "BAR",
        }
    }

    assert (
        filesystem_manager.files[TEMPLATE_FILES[template_type].value] == expected_data
    )


def test_store_generated_place_command_location_without_type_raises_key_error():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestLocation"),
        description=RequiredString("A test location"),
        categories=[RequiredString("Category1"), RequiredString("Category2")],
        type=None,
    )
    template_type = TemplateType.LOCATION
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute and Verify
    with pytest.raises(KeyError) as exc_info:
        command.execute()
    assert (
        "Was tasked with storing a location, but the place data didn't contain the 'type' key."
        in str(exc_info.value)
    )


def test_store_generated_place_command_updates_existing_file():
    # Setup
    initial_data = {
        "ExistingPlace": {
            "description": "An existing place",
            "categories": ["existingcategory"],
        }
    }
    place_data = PlaceData(
        name=RequiredString("NewPlace"),
        description=RequiredString("A new place"),
        categories=[RequiredString("Category1")],
        type=None,
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()
    filesystem_manager.files[TEMPLATE_FILES[template_type].value] = initial_data

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    command.execute()

    # Verify
    expected_data = {
        "ExistingPlace": {
            "description": "An existing place",
            "categories": ["existingcategory"],
        },
        "NewPlace": {
            "description": "A new place",
            "categories": ["category1"],
        },
    }

    assert (
        filesystem_manager.files[TEMPLATE_FILES[template_type].value] == expected_data
    )


def test_store_generated_place_command_logging(caplog):
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[RequiredString("Category1")],
        type=None,
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    with caplog.at_level(logging.INFO):
        command.execute()

    # Verify
    assert f"Saved {template_type.value} template 'TestPlace'." in caplog.text


def test_store_generated_place_command_empty_categories():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[],
        type=None,
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute
    command.execute()

    # Verify
    expected_data = {
        "TestPlace": {
            "description": "A test place",
            "categories": [],
        }
    }

    assert (
        filesystem_manager.files[TEMPLATE_FILES[template_type].value] == expected_data
    )


def test_store_generated_place_command_save_raises_exception():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[RequiredString("Category1")],
        type=None,
    )
    template_type = TemplateType.AREA

    filesystem_manager = MockFilesystemManager()

    def mock_save_json_file(data, filename):
        raise IOError("Failed to save file")

    filesystem_manager.save_json_file = mock_save_json_file

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute and Verify
    with pytest.raises(IOError) as exc_info:
        command.execute()
    assert "Failed to save file" in str(exc_info.value)


def test_store_generated_place_command_load_raises_exception():
    # Setup
    place_data = PlaceData(
        name=RequiredString("TestPlace"),
        description=RequiredString("A test place"),
        categories=[RequiredString("Category1")],
        type=None,
    )
    template_type = TemplateType.AREA

    filesystem_manager = MockFilesystemManager()

    def mock_load_existing_or_new_json_file(filename):
        raise IOError("Failed to load file")

    filesystem_manager.load_existing_or_new_json_file = (
        mock_load_existing_or_new_json_file
    )

    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )

    # Execute and Verify
    with pytest.raises(IOError) as exc_info:
        command.execute()
    assert "Failed to load file" in str(exc_info.value)
