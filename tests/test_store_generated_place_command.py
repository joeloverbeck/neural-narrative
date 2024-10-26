import logging
from enum import Enum
from pathlib import Path
from unittest.mock import patch

import pytest

from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.maps.place_data import PlaceData


def test_execute_adds_place_data_correctly():
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place.",
        categories=["Category1", "Category2"],
        type=None,  # Not needed for non-LOCATION types
    )
    template_type = TemplateType.AREA  # Non-LOCATION type
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    # Mock the file operations
    mock_template_file = {}

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ) as mock_read_json_file:
        with patch(
            "src.maps.commands.store_generated_place_command.write_json_file"
        ) as mock_write_json_file:
            # Act
            command.execute()

            # Assert
            expected_data = {
                place_data.name: {
                    "description": place_data.description,
                    "categories": [c.lower() for c in place_data.categories],
                }
            }
            expected_file_path = Path(TEMPLATE_FILES.get(template_type))
            mock_read_json_file.assert_called_once_with(expected_file_path)
            mock_write_json_file.assert_called_once_with(
                expected_file_path, expected_data
            )


def test_execute_adds_place_data_with_type_for_location():
    # Arrange
    place_data = PlaceData(
        name="Test Location",
        description="A test location.",
        categories=["Category1", "Category2"],
        type="TestType",
    )
    template_type = TemplateType.LOCATION
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = {}

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ) as mock_read_json_file:
        with patch(
            "src.maps.commands.store_generated_place_command.write_json_file"
        ) as mock_write_json_file:
            # Act
            command.execute()

            # Assert
            expected_data = {
                place_data.name: {
                    "description": place_data.description,
                    "categories": [c.lower() for c in place_data.categories],
                    "type": place_data.type,
                }
            }
            expected_file_path = Path(TEMPLATE_FILES.get(template_type))
            mock_read_json_file.assert_called_once_with(expected_file_path)
            mock_write_json_file.assert_called_once_with(
                expected_file_path, expected_data
            )


def test_execute_raises_keyerror_when_type_missing_for_location():
    # Arrange
    place_data = PlaceData(
        name="Test Location",
        description="A test location.",
        categories=["Category1", "Category2"],
        type=None,  # Missing type
    )
    template_type = TemplateType.LOCATION
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = {}

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ):
        # Act & Assert
        with pytest.raises(
            KeyError,
            match="Was tasked with storing a location, but the place data didn't contain the 'type' key.",
        ):
            command.execute()


def test_execute_updates_existing_template_file():
    # Arrange
    existing_place_name = "Existing Place"
    existing_place_data = {
        existing_place_name: {
            "description": "An existing place.",
            "categories": ["existingcategory"],  # noqa
        }
    }

    new_place_name = "New Place"
    place_data = PlaceData(
        name=new_place_name,
        description="A new place.",
        categories=["NewCategory1", "NewCategory2"],
        type=None,
    )
    template_type = TemplateType.AREA
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = existing_place_data.copy()

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ) as mock_read_json_file:
        with patch(
            "src.maps.commands.store_generated_place_command.write_json_file"
        ) as mock_write_json_file:
            # Act
            command.execute()

            # Assert
            expected_data = existing_place_data.copy()
            expected_data.update(
                {
                    new_place_name: {
                        "description": place_data.description,
                        "categories": [c.lower() for c in place_data.categories],
                    }
                }
            )
            expected_file_path = Path(TEMPLATE_FILES.get(template_type))
            mock_read_json_file.assert_called_once_with(expected_file_path)
            mock_write_json_file.assert_called_once_with(
                expected_file_path, expected_data
            )


def test_execute_updates_existing_place_data():
    # Arrange
    place_name = "Test Place"
    existing_place_data = {
        place_name: {
            "description": "Old description.",
            "categories": ["oldcategory"],  # noqa
        }
    }

    place_data = PlaceData(
        name=place_name,
        description="New description.",
        categories=["NewCategory"],
        type=None,
    )
    template_type = TemplateType.AREA
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = existing_place_data.copy()

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ) as mock_read_json_file:
        with patch(
            "src.maps.commands.store_generated_place_command.write_json_file"
        ) as mock_write_json_file:
            # Act
            command.execute()

            # Assert
            expected_data = {
                place_name: {
                    "description": place_data.description,
                    "categories": [c.lower() for c in place_data.categories],
                }
            }
            expected_file_path = Path(TEMPLATE_FILES.get(template_type))
            mock_read_json_file.assert_called_once_with(expected_file_path)
            mock_write_json_file.assert_called_once_with(
                expected_file_path, expected_data
            )


def test_execute_with_empty_categories():
    # Arrange
    place_data = PlaceData(
        name="Test Place", description="A test place.", categories=[], type=None
    )
    template_type = TemplateType.AREA
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = {}

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ) as mock_read_json_file:
        with patch(
            "src.maps.commands.store_generated_place_command.write_json_file"
        ) as mock_write_json_file:
            # Act
            command.execute()

            # Assert
            expected_data = {
                place_data.name: {
                    "description": place_data.description,
                    "categories": [],
                }
            }
            expected_file_path = Path(TEMPLATE_FILES.get(template_type))
            mock_read_json_file.assert_called_once_with(expected_file_path)
            mock_write_json_file.assert_called_once_with(
                expected_file_path, expected_data
            )


def test_execute_logs_info_message(caplog):
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA
    command = StoreGeneratedPlaceCommand(place_data, template_type)

    mock_template_file = {}

    with patch(
        "src.maps.commands.store_generated_place_command.read_json_file",
        return_value=mock_template_file,
    ):
        with patch("src.maps.commands.store_generated_place_command.write_json_file"):
            # Act
            with caplog.at_level(logging.INFO):
                command.execute()

                # Assert
                expected_message = (
                    f"Saved {template_type} template '{place_data.name}'."
                )
                assert expected_message in caplog.text


def test_execute_raises_exception_when_template_file_not_found():
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place.",
        categories=["Category1", "Category2"],
        type=None,
    )

    # Create an invalid template type that's not in TEMPLATE_FILES
    class InvalidTemplateType(Enum):
        INVALID = "invalid"

    invalid_template_type = InvalidTemplateType.INVALID
    command = StoreGeneratedPlaceCommand(place_data, invalid_template_type)  # noqa

    # Act & Assert
    with pytest.raises(TypeError):
        command.execute()
