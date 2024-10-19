import logging
from unittest.mock import MagicMock, patch

import pytest

from src.base.commands.generate_story_universe_command import (
    GenerateStoryUniverseCommand,
)
from src.base.constants import STORY_UNIVERSES_TEMPLATE_FILE
from src.base.exceptions import StoryUniverseGenerationError
from src.base.factories.story_universe_factory import StoryUniverseFactory
from src.base.playthrough_name import RequiredString
from src.base.products.story_universe_product import StoryUniverseProduct
from src.filesystem.filesystem_manager import FilesystemManager


def test_execute_success():
    """Test that the command executes successfully and saves the product."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    command.execute()

    # Assert
    mock_product.get_name.assert_called()
    mock_product.get_description.assert_called()
    mock_product.get_categories.assert_called()
    mock_filesystem_manager.load_existing_or_new_json_file.assert_called_with(
        STORY_UNIVERSES_TEMPLATE_FILE
    )
    expected_data = {
        "UniverseName": {
            "description": "UniverseDescription",
            "categories": ["Category1", "Category2"],
        }
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


def test_execute_product_generation_error(caplog):
    """Test that a StoryUniverseGenerationError is raised when product generation fails."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_factory.generate_product.side_effect = ValueError("Invalid product data")

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act & Assert
    with pytest.raises(StoryUniverseGenerationError) as exc_info:
        with caplog.at_level(logging.ERROR):
            command.execute()

    assert "Failed to generate a story universe. Error: Invalid product data" in str(
        exc_info.value
    )
    assert (
        "Failed to generate a story universe. Error: Invalid product data"
        in caplog.text
    )


def test_execute_updates_existing_file():
    """Test that the command updates an existing JSON file with new data."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    existing_data = {
        "ExistingUniverse": {
            "description": "ExistingDescription",
            "categories": ["ExistingCategory1", "ExistingCategory2"],
        }
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = existing_data

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    command.execute()

    # Assert
    expected_data = existing_data.copy()
    expected_data["UniverseName"] = {
        "description": "UniverseDescription",
        "categories": ["Category1", "Category2"],
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


def test_execute_logs_info_on_success(caplog):
    """Test that an info log is recorded upon successful execution."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    with caplog.at_level(logging.INFO):
        command.execute()

    # Assert
    assert "Saved story universe 'UniverseName'." in caplog.text


def test_execute_save_json_file_raises_exception():
    """Test that an exception from save_json_file propagates."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_filesystem_manager.save_json_file.side_effect = IOError("Unable to save file")

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act & Assert
    with pytest.raises(IOError) as exc_info:
        command.execute()

    assert "Unable to save file" in str(exc_info.value)


def test_execute_overwrites_existing_universe():
    """Test that an existing universe is overwritten with new data."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("ExistingUniverse")
    mock_product.get_description.return_value = RequiredString("NewDescription")
    mock_product.get_categories.return_value = [
        RequiredString("NewCategory1"),
        RequiredString("NewCategory2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    existing_data = {
        "ExistingUniverse": {
            "description": "OldDescription",
            "categories": ["OldCategory1", "OldCategory2"],
        }
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = existing_data

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    command.execute()

    # Assert
    expected_data = existing_data.copy()
    expected_data["ExistingUniverse"] = {
        "description": "NewDescription",
        "categories": ["NewCategory1", "NewCategory2"],
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


def test_execute_product_with_invalid_name():
    """Test that an AttributeError is raised when product name is invalid."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = None  # Invalid name
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act & Assert
    with pytest.raises(AttributeError) as exc_info:
        command.execute()

    assert "'NoneType' object has no attribute 'value'" in str(exc_info.value)


def test_execute_product_with_no_categories():
    """Test that the command handles a product with no categories."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = []
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        "UniverseName": {
            "description": "UniverseDescription",
            "categories": [],
        }
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


def test_execute_with_unicode_characters():
    """Test that the command handles Unicode characters properly."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("宇宙")
    mock_product.get_description.return_value = RequiredString("这是一个描述")
    mock_product.get_categories.return_value = [
        RequiredString("类别1"),
        RequiredString("类别2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    command.execute()

    # Assert
    expected_data = {
        "宇宙": {
            "description": "这是一个描述",
            "categories": ["类别1", "类别2"],
        }
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


def test_execute_with_default_filesystem_manager():
    """Test that the default FilesystemManager is used when none is provided."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    with patch(
        "src.base.commands.generate_story_universe_command.FilesystemManager"
    ) as MockFilesystemManager:
        mock_filesystem_manager_instance = MockFilesystemManager.return_value
        mock_filesystem_manager_instance.load_existing_or_new_json_file.return_value = (
            {}
        )

        command = GenerateStoryUniverseCommand(story_universe_factory=mock_factory)

        # Act
        command.execute()

        # Assert
        MockFilesystemManager.assert_called_once()
        mock_filesystem_manager_instance.load_existing_or_new_json_file.assert_called_with(
            STORY_UNIVERSES_TEMPLATE_FILE
        )
        expected_data = {
            "UniverseName": {
                "description": "UniverseDescription",
                "categories": ["Category1", "Category2"],
            }
        }
        mock_filesystem_manager_instance.save_json_file.assert_called_with(
            expected_data, STORY_UNIVERSES_TEMPLATE_FILE
        )


def test_execute_with_invalid_story_universes_file():
    """Test that a TypeError is raised when the loaded JSON file is invalid."""
    # Arrange
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = RequiredString("UniverseName")
    mock_product.get_description.return_value = RequiredString("UniverseDescription")
    mock_product.get_categories.return_value = [
        RequiredString("Category1"),
        RequiredString("Category2"),
    ]
    mock_factory.generate_product.return_value = mock_product

    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = (
        None  # Invalid
    )

    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act & Assert
    with pytest.raises(TypeError) as exc_info:
        command.execute()

    assert "'NoneType' object does not support item assignment" in str(exc_info.value)
