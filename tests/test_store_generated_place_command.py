import logging
from typing import cast
import pytest
from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.maps.place_data import PlaceData


class MockFilesystemManager:

    def __init__(self):
        self.files = {}

    def load_existing_or_new_json_file(self, filename: str):
        if filename is None:
            raise ValueError("Filename cannot be None")
        return self.files.get(filename, {})

    def save_json_file(self, data, filename: str):
        if filename is None:
            raise ValueError("Filename cannot be None")
        self.files[filename] = data


def test_store_generated_place_command_normal_case():
    place_data = PlaceData(
        name="TestPlace",
        description="A test place",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.REGION
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    command.execute()
    expected_data = {
        "TestPlace": {
            "description": "A test place",
            "categories": ["category1", "category2"],
        }
    }
    assert filesystem_manager.files[TEMPLATE_FILES[template_type]] == expected_data


def test_store_generated_place_command_categories_lowercase():
    place_data = PlaceData(
        name="TestPlace",
        description="A test place",
        categories=["Category1", "CATEGORY2"],
        type=None,
    )
    template_type = TemplateType.REGION
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    command.execute()
    saved_data = filesystem_manager.files[TEMPLATE_FILES[template_type]]
    categories = saved_data["TestPlace"]["categories"]
    assert categories == ["category1", "category2"]


def test_store_generated_place_command_location_with_type():
    place_data = PlaceData(
        name="TestLocation",
        description="A test location",
        categories=["Category1", "Category2"],
        type="BAR",
    )
    template_type = TemplateType.LOCATION
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    command.execute()
    expected_data = {
        "TestLocation": {
            "description": "A test location",
            "categories": ["category1", "category2"],
            "type": "BAR",
        }
    }
    assert filesystem_manager.files[TEMPLATE_FILES[template_type]] == expected_data


def test_store_generated_place_command_location_without_type_raises_key_error():
    place_data = PlaceData(
        name="TestLocation",
        description="A test location",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.LOCATION
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    with pytest.raises(KeyError) as exc_info:
        command.execute()
    assert (
        "Was tasked with storing a location, but the place data didn't contain the 'type' key."
        in str(exc_info)
    )


def test_store_generated_place_command_updates_existing_file():
    initial_data = {
        "ExistingPlace": {
            "description": "An existing place",
            "categories": ["existingcategory"],
        }
    }
    place_data = PlaceData(
        name="NewPlace", description="A new place", categories=["Category1"], type=None
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()
    filesystem_manager.files[TEMPLATE_FILES[template_type]] = initial_data
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    command.execute()
    expected_data = {
        "ExistingPlace": {
            "description": "An existing place",
            "categories": ["existingcategory"],
        },
        "NewPlace": {"description": "A new place", "categories": ["category1"]},
    }
    assert filesystem_manager.files[TEMPLATE_FILES[template_type]] == expected_data


def test_store_generated_place_command_logging(caplog):
    place_data = PlaceData(
        name="TestPlace",
        description="A test place",
        categories=["Category1"],
        type=None,
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    with caplog.at_level(logging.INFO):
        command.execute()
    assert f"Saved {template_type} template 'TestPlace'." in caplog.text


def test_store_generated_place_command_empty_categories():
    place_data = PlaceData(
        name="TestPlace", description="A test place", categories=[], type=None
    )
    template_type = TemplateType.AREA
    filesystem_manager = MockFilesystemManager()
    command = StoreGeneratedPlaceCommand(
        place_data, template_type, cast(FilesystemManager, filesystem_manager)
    )
    command.execute()
    expected_data = {"TestPlace": {"description": "A test place", "categories": []}}
    assert filesystem_manager.files[TEMPLATE_FILES[template_type]] == expected_data


def test_store_generated_place_command_save_raises_exception():
    place_data = PlaceData(
        name="TestPlace",
        description="A test place",
        categories=["Category1"],
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
    with pytest.raises(IOError) as exc_info:
        command.execute()
    assert "Failed to save file" in str(exc_info)


def test_store_generated_place_command_load_raises_exception():
    place_data = PlaceData(
        name="TestPlace",
        description="A test place",
        categories=["Category1"],
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
    with pytest.raises(IOError) as exc_info:
        command.execute()
    assert "Failed to load file" in str(exc_info)
