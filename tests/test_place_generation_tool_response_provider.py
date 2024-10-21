from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.base.required_string import RequiredString
from src.maps.template_type_data import TemplateTypeData
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


def test_get_prompt_file_world():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )

    # Mock the TemplateTypeData returned by _get_template_type_data
    provider._get_template_type_data = Mock(
        return_value=TemplateTypeData(
            prompt_file=RequiredString("world_prompt_file"),
            father_templates_file_path=RequiredString("father_templates_file"),
            current_place_templates_file_path=RequiredString(
                "current_place_templates_file"
            ),
            tool_file=RequiredString("world_tool_file"),
        )
    )

    # Act
    prompt_file = provider.get_prompt_file()

    # Assert
    assert prompt_file == RequiredString("world_prompt_file")


def test_get_prompt_file_template_data_none():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )

    # Mock _get_template_type_data to return None
    provider._get_template_type_data = Mock(return_value=None)

    # Act and Assert
    with pytest.raises(ValueError) as exc_info:
        prompt_file = provider.get_prompt_file()
    assert (
        f"Failed to produce template data for father place identifier '{father_place_identifier.value}' and template type {template_type.value}."
        in str(exc_info.value)
    )


def test_get_prompt_kwargs():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )

    # Mock TemplateTypeData
    template_data = TemplateTypeData(
        prompt_file=RequiredString("world_prompt_file"),
        father_templates_file_path=RequiredString("father_templates_file"),
        current_place_templates_file_path=RequiredString(
            "current_place_templates_file"
        ),
        tool_file=RequiredString("world_tool_file"),
    )
    provider._get_template_type_data = Mock(return_value=template_data)

    # Mock filesystem_manager.load_existing_or_new_json_file
    father_templates_file_data = {
        "some_father_place": {
            "description": "Father place description",
            "categories": ["category1", "category2"],
        }
    }
    current_place_type_templates = {"place1": {}, "place2": {}}

    filesystem_manager.load_existing_or_new_json_file.side_effect = [
        father_templates_file_data,
        current_place_type_templates,
    ]

    # Act
    prompt_kwargs = provider.get_prompt_kwargs()

    # Assert
    expected_prompt_kwargs = {
        "father_place_name": "some_father_place",
        "father_place_description": "Father place description",
        "father_place_categories": ["category1", "category2"],
        "current_place_type_names": ["place1", "place2"],
    }
    assert prompt_kwargs == expected_prompt_kwargs


def test_get_tool_file():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )

    # Mock TemplateTypeData
    template_data = TemplateTypeData(
        prompt_file=RequiredString("world_prompt_file"),
        father_templates_file_path=RequiredString("father_templates_file"),
        current_place_templates_file_path=RequiredString(
            "current_place_templates_file"
        ),
        tool_file=RequiredString("world_tool_file"),
    )
    provider._get_template_type_data = Mock(return_value=template_data)

    # Act
    tool_file = provider.get_tool_file()

    # Assert
    assert tool_file == RequiredString("world_tool_file")


def test_get_user_content_with_notion():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )

    # Act
    user_content = provider.get_user_content()

    # Assert
    expected_content = "Create the name and description of a world, following the above instructions. User guidance about how he wants this place to be: some notion"
    assert user_content == expected_content


def test_create_product():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = RequiredString("some_father_place")
    template_type = TemplateType.WORLD
    notion = RequiredString("some notion")
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        produce_tool_response_strategy_factory,
        filesystem_manager,
    )
    arguments = {"key": "value"}

    # Act
    product = provider.create_product(arguments)

    # Assert
    assert isinstance(product, ConcreteLlmToolResponseProduct)
    assert product.get() == arguments
    assert product.is_valid() == True


def test_read_and_format_tool_file_other():
    # Arrange
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    filesystem_manager.read_json_file.return_value = {"some_key": "some_value"}

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier=RequiredString("some_father_place"),
        template_type=TemplateType.AREA,
        notion=RequiredString("some notion"),
        produce_tool_response_strategy_factory=produce_tool_response_strategy_factory,
        filesystem_manager=filesystem_manager,
    )

    # Act
    tool_file = "some_other_tool_file.json"
    result = provider._read_and_format_tool_file(tool_file)

    # Assert
    filesystem_manager.read_json_file.assert_called_once_with(tool_file)
    assert result == {"some_key": "some_value"}
