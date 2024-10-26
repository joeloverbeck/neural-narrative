import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.base.commands.generate_story_universe_command import (
    GenerateStoryUniverseCommand,
)
from src.base.constants import STORY_UNIVERSES_TEMPLATE_FILE
from src.base.exceptions import StoryUniverseGenerationError
from src.base.factories.story_universe_factory import StoryUniverseFactory
from src.base.products.story_universe_product import StoryUniverseProduct
from src.filesystem.filesystem_manager import FilesystemManager


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_success(mock_json_file):
    """Test that the command executes successfully and saves the product."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = ["Category1", "Category2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_json_file.return_value = {}
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    command.execute()
    mock_product.get_name.assert_called()
    mock_product.get_description.assert_called()
    mock_product.get_categories.assert_called()
    mock_json_file.assert_called_with(Path(STORY_UNIVERSES_TEMPLATE_FILE))
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
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_factory.generate_product.side_effect = ValueError("Invalid product data")
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    with pytest.raises(StoryUniverseGenerationError) as exc_info:
        with caplog.at_level(logging.ERROR):
            command.execute()
    assert "Failed to generate a story universe. Error: Invalid product data" in str(
        exc_info
    )
    assert (
        "Failed to generate a story universe. Error: Invalid product data"
        in caplog.text
    )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_updates_existing_file(mock_read_json_file):
    """Test that the command updates an existing JSON file with new data."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = ["Category1", "Category2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    existing_data = {
        "ExistingUniverse": {
            "description": "ExistingDescription",
            "categories": ["ExistingCategory1", "ExistingCategory2"],
        }
    }
    mock_read_json_file.return_value = existing_data
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    command.execute()
    expected_data = existing_data.copy()
    expected_data["UniverseName"] = {
        "description": "UniverseDescription",
        "categories": ["Category1", "Category2"],
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_save_json_file_raises_exception(mock_read_json_file):
    """Test that an exception from save_json_file propagates."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = ["Category1", "Category2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_json_file.return_value = {}
    mock_filesystem_manager.save_json_file.side_effect = IOError("Unable to save file")
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    with pytest.raises(IOError) as exc_info:
        command.execute()
    assert "Unable to save file" in str(exc_info)


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_overwrites_existing_universe(mock_read_json_file):
    """Test that an existing universe is overwritten with new data."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "ExistingUniverse"
    mock_product.get_description.return_value = "NewDescription"
    mock_product.get_categories.return_value = ["NewCategory1", "NewCategory2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    existing_data = {
        "ExistingUniverse": {
            "description": "OldDescription",
            "categories": ["OldCategory1", "OldCategory2"],
        }
    }
    mock_read_json_file.return_value = existing_data
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    command.execute()
    expected_data = existing_data.copy()
    expected_data["ExistingUniverse"] = {
        "description": "NewDescription",
        "categories": ["NewCategory1", "NewCategory2"],
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_product_with_invalid_name(_mock_read_json_file):
    """Test that an AttributeError is raised when product name is invalid."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = None
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "must be a non-empty string." in str(exc_info)


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_product_with_no_categories(mock_read_json_file):
    """Test that the command handles a product with no categories."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = []
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_json_file.return_value = {}
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    command.execute()
    expected_data = {
        "UniverseName": {"description": "UniverseDescription", "categories": []}
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_with_unicode_characters(mock_read_json_file):
    """Test that the command handles Unicode characters properly."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "宇宙"
    mock_product.get_description.return_value = "这是一个描述"
    mock_product.get_categories.return_value = ["类别1", "类别2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_json_file.return_value = {}
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    command.execute()
    expected_data = {
        "宇宙": {"description": "这是一个描述", "categories": ["类别1", "类别2"]}
    }
    mock_filesystem_manager.save_json_file.assert_called_with(
        expected_data, STORY_UNIVERSES_TEMPLATE_FILE
    )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_with_default_filesystem_manager(mock_read_json_file):
    """Test that the default FilesystemManager is used when none is provided."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = ["Category1", "Category2"]
    mock_factory.generate_product.return_value = mock_product
    with patch(
        "src.base.commands.generate_story_universe_command.FilesystemManager"
    ) as MockFilesystemManager:
        mock_filesystem_manager_instance = MockFilesystemManager.return_value
        (mock_read_json_file.return_value) = {}
        command = GenerateStoryUniverseCommand(story_universe_factory=mock_factory)
        command.execute()
        MockFilesystemManager.assert_called_once()
        mock_read_json_file.assert_called_with(Path(STORY_UNIVERSES_TEMPLATE_FILE))
        expected_data = {
            "UniverseName": {
                "description": "UniverseDescription",
                "categories": ["Category1", "Category2"],
            }
        }
        mock_filesystem_manager_instance.save_json_file.assert_called_with(
            expected_data, STORY_UNIVERSES_TEMPLATE_FILE
        )


@patch("src.base.commands.generate_story_universe_command.read_json_file")
def test_execute_with_invalid_story_universes_file(mock_read_json_file):
    """Test that a TypeError is raised when the loaded JSON file is invalid."""
    mock_factory = MagicMock(spec=StoryUniverseFactory)
    mock_product = MagicMock(spec=StoryUniverseProduct)
    mock_product.get_name.return_value = "UniverseName"
    mock_product.get_description.return_value = "UniverseDescription"
    mock_product.get_categories.return_value = ["Category1", "Category2"]
    mock_factory.generate_product.return_value = mock_product
    mock_filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_json_file.return_value = None
    command = GenerateStoryUniverseCommand(
        story_universe_factory=mock_factory, filesystem_manager=mock_filesystem_manager
    )
    with pytest.raises(TypeError) as exc_info:
        command.execute()
    assert "'NoneType' object does not support item assignment" in str(exc_info)
