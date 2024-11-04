import logging
from unittest.mock import MagicMock, patch

import pytest

from src.base.enums import TemplateType
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.maps.place_data import PlaceData


def test_execute_adds_place_data_correctly():
    """
    Test that the execute method adds place data correctly for a template type that doesn't require 'type'.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA  # Does not require 'type'

    # Mock TemplatesRepository
    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    # Create command instance
    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        place_data.name: {
            "description": place_data.description,
            "categories": [c.lower() for c in place_data.categories],
        }
    }
    mock_templates_repository.load_templates.assert_called_once_with(template_type)
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_execute_adds_place_data_with_type_for_location():
    """
    Test that the execute method adds 'type' to the place data for LOCATION template types.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Location",
        description="A test location description.",
        categories=["Category1", "Category2"],
        type="City",
    )
    template_type = TemplateType.LOCATION

    # Mock TemplatesRepository
    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    # Create command instance
    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

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
    mock_templates_repository.load_templates.assert_called_once_with(template_type)
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_execute_raises_key_error_when_type_missing_for_location():
    """
    Test that a KeyError is raised when 'type' is missing for LOCATION or ROOM template types.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Location",
        description="A test location description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.LOCATION

    # Mock TemplatesRepository
    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act & Assert
    with pytest.raises(KeyError) as exc_info:
        command.execute()

    expected_error_msg = f"Was tasked with storing a {template_type.value}, but the place data didn't contain the 'type' key."
    assert expected_error_msg in str(exc_info.value)


def test_execute_does_not_raise_error_when_type_missing_for_area():
    """
    Test that no error is raised when 'type' is missing for template types that do not require it.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Area",
        description="A test area description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA

    # Mock TemplatesRepository
    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        place_data.name: {
            "description": place_data.description,
            "categories": [c.lower() for c in place_data.categories],
        }
    }
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_templates_repository_methods_called_correctly():
    """
    Test that TemplatesRepository methods are called with correct parameters.
    """
    # Arrange
    place_data = PlaceData(
        name="Test World",
        description="A test world description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.WORLD

    # Mock TemplatesRepository
    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    mock_templates_repository.load_templates.assert_called_once_with(template_type)
    mock_templates_repository.save_templates.assert_called_once()
    args, kwargs = mock_templates_repository.save_templates.call_args
    assert args[0] == template_type
    assert place_data.name in args[1]


def test_categories_are_lowercased():
    """
    Test that categories are stored in lowercase.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=["Category1", "CATEGORY2", "category3"],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_categories = [c.lower() for c in place_data.categories]
    saved_data = mock_templates_repository.save_templates.call_args[0][1]
    assert saved_data[place_data.name]["categories"] == expected_categories


def test_logger_info_called_with_correct_message(caplog):
    """
    Test that logger.info is called with the correct message.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    with caplog.at_level(logging.INFO):
        command.execute()

    # Assert
    expected_message = f"Saved {template_type} template '{place_data.name}'."
    assert expected_message in caplog.text


def test_templates_repository_defaults_to_new_instance():
    """
    Test that a new TemplatesRepository instance is created if none is provided.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA

    with patch(
        "src.maps.commands.store_generated_place_command.TemplatesRepository"
    ) as MockTemplatesRepo:
        mock_templates_repository_instance = MockTemplatesRepo.return_value
        mock_templates_repository_instance.load_templates.return_value = {}

        command = StoreGeneratedPlaceCommand(
            place_data=place_data, template_type=template_type
        )

        # Act
        command.execute()

        # Assert
        MockTemplatesRepo.assert_called_once()
        mock_templates_repository_instance.load_templates.assert_called_once_with(
            template_type
        )
        mock_templates_repository_instance.save_templates.assert_called_once()


def test_existing_templates_data_is_preserved():
    """
    Test that existing data in templates is preserved when new place data is added.
    """
    # Arrange
    existing_data = {
        "Existing Place": {
            "description": "An existing place.",
            "categories": ["existing"],
        }
    }
    place_data = PlaceData(
        name="New Place",
        description="A new place description.",
        categories=["Category1", "Category2"],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = existing_data.copy()

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_data = existing_data.copy()
    expected_data.update(
        {
            place_data.name: {
                "description": place_data.description,
                "categories": [c.lower() for c in place_data.categories],
            }
        }
    )
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_execute_with_empty_categories():
    """
    Test that execute method works correctly when categories list is empty.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=[],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        place_data.name: {"description": place_data.description, "categories": []}
    }
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_execute_overwrites_existing_place_data():
    """
    Test that existing place data is overwritten when a place with the same name is stored.
    """
    # Arrange
    existing_data = {
        "Test Place": {"description": "Old description.", "categories": ["oldcategory"]}
    }
    place_data = PlaceData(
        name="Test Place",
        description="New description.",
        categories=["NewCategory"],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = existing_data.copy()

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        "Test Place": {"description": "New description.", "categories": ["newcategory"]}
    }
    mock_templates_repository.save_templates.assert_called_once_with(
        template_type, expected_data
    )


def test_execute_propagates_exception_from_save_templates():
    """
    Test that an exception from save_templates is propagated up.
    """
    # Arrange
    place_data = PlaceData(
        name="Test Place",
        description="A test place description.",
        categories=["Category1"],
        type=None,
    )
    template_type = TemplateType.AREA

    mock_templates_repository = MagicMock()
    mock_templates_repository.load_templates.return_value = {}
    mock_templates_repository.save_templates.side_effect = IOError(
        "Failed to save templates"
    )

    command = StoreGeneratedPlaceCommand(
        place_data=place_data,
        template_type=template_type,
        templates_repository=mock_templates_repository,
    )

    # Act & Assert
    with pytest.raises(IOError) as exc_info:
        command.execute()

    assert str(exc_info.value) == "Failed to save templates"
