from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.base.constants import PARENT_TEMPLATE_TYPE, TEMPLATE_FILES
from src.base.enums import TemplateType
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


def test_init_valid_inputs():
    """Test initialization with valid inputs."""
    place_template_type = TemplateType.AREA
    father_place_template_type = TemplateType.REGION
    father_place_name = "USA"
    place_generation_tool_response_provider = Mock(
        spec=PlaceGenerationToolResponseProvider
    )
    store_generated_place_command_factory = Mock(spec=StoreGeneratedPlaceCommandFactory)
    with patch("src.base.constants.PARENT_TEMPLATE_TYPE", PARENT_TEMPLATE_TYPE):
        command = GeneratePlaceCommand(
            place_template_type,
            father_place_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        )
        assert command is not None


def test_init_mismatched_father_place_template_type():
    """Test initialization with mismatched father_place_template_type."""
    place_template_type = TemplateType.AREA
    father_place_template_type = TemplateType.AREA
    father_place_name = "New York"
    place_generation_tool_response_provider = Mock(
        spec=PlaceGenerationToolResponseProvider
    )
    store_generated_place_command_factory = Mock(spec=StoreGeneratedPlaceCommandFactory)
    with pytest.raises(
        ValueError,
        match="Attempted to create a 'area' from something other than a 'region'",
    ):
        GeneratePlaceCommand(
            place_template_type,
            father_place_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        )


@patch("src.maps.commands.generate_place_command.read_json_file")
def test_execute_valid(mock_read_json_file):
    """Test execute method with valid inputs."""
    place_template_type = TemplateType.AREA
    father_place_template_type = TemplateType.REGION
    father_place_name = "USA"
    place_generation_tool_response_provider = Mock(
        spec=PlaceGenerationToolResponseProvider
    )
    store_generated_place_command_factory = Mock(spec=StoreGeneratedPlaceCommandFactory)
    llm_tool_response_product = Mock()
    llm_tool_response_product.is_valid.return_value = True
    place_data = {"name": "New York", "description": "A stinking big city."}
    llm_tool_response_product.get.return_value = place_data
    (place_generation_tool_response_provider.generate_product.return_value) = (
        llm_tool_response_product
    )
    father_place_templates = {"USA": {"categories": ["Economy", "Culture"]}}
    mock_read_json_file.return_value = father_place_templates
    store_generated_place_command = Mock()
    store_generated_place_command_factory.create_command.return_value = (
        store_generated_place_command
    )
    with patch("src.base.constants.PARENT_TEMPLATE_TYPE", PARENT_TEMPLATE_TYPE), patch(
        "src.base.constants.TEMPLATE_FILES", TEMPLATE_FILES
    ):
        command = GeneratePlaceCommand(
            place_template_type,
            father_place_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        )
        command.execute()
        place_generation_tool_response_provider.generate_product.assert_called_once()
        llm_tool_response_product.is_valid.assert_called_once()
        llm_tool_response_product.get.assert_called_once()
        mock_read_json_file.assert_called_once_with(
            Path(TEMPLATE_FILES[father_place_template_type])
        )
        store_generated_place_command.execute.assert_called_once()


@patch("src.maps.commands.generate_place_command.read_json_file")
def test_execute_father_place_name_not_in_templates(mock_read_json_file):
    """Test execute method when father_place_name is not in templates."""
    place_template_type = TemplateType.AREA
    father_place_template_type = TemplateType.REGION
    father_place_name = "Unknown Country"
    place_generation_tool_response_provider = Mock(
        spec=PlaceGenerationToolResponseProvider
    )
    store_generated_place_command_factory = Mock(spec=StoreGeneratedPlaceCommandFactory)
    father_place_templates = {"USA": {"categories": ["Economy", "Culture"]}}
    mock_read_json_file.return_value = father_place_templates
    with patch("src.base.constants.TEMPLATE_FILES", TEMPLATE_FILES):
        command = GeneratePlaceCommand(
            place_template_type,
            father_place_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        )
        with pytest.raises(
            ValueError,
            match=f"There isn't a '{father_place_template_type}' template named '{father_place_name}'.",
        ):
            command.execute()


@patch("src.maps.commands.generate_place_command.read_json_file")
def test_execute_llm_tool_response_invalid(mock_read_json_file):
    """Test execute method when LLM tool response is invalid."""
    place_template_type = TemplateType.AREA
    father_place_template_type = TemplateType.REGION
    father_place_name = "USA"
    place_generation_tool_response_provider = Mock(
        spec=PlaceGenerationToolResponseProvider
    )
    store_generated_place_command_factory = Mock(spec=StoreGeneratedPlaceCommandFactory)
    llm_tool_response_product = Mock()
    llm_tool_response_product.is_valid.return_value = False
    llm_tool_response_product.get_error.return_value = "Some error occurred"
    (place_generation_tool_response_provider.generate_product.return_value) = (
        llm_tool_response_product
    )
    father_place_templates = {"USA": {"categories": ["Economy", "Culture"]}}
    mock_read_json_file.return_value = father_place_templates
    with patch("src.base.constants.TEMPLATE_FILES", TEMPLATE_FILES):
        command = GeneratePlaceCommand(
            place_template_type,
            father_place_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        )
        with pytest.raises(
            ValueError,
            match="Unable to produce a tool response for 'area' generation: Some error occurred",
        ):
            command.execute()
