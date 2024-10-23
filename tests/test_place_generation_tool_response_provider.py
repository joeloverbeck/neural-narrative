from typing import cast
from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.maps.template_type_data import TemplateTypeData
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


def test_get_prompt_file_world():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    provider._get_template_type_data = Mock(
        return_value=TemplateTypeData(
            prompt_file="world_prompt_file",
            father_templates_file_path="father_templates_file",
            current_place_templates_file_path="current_place_templates_file",
            tool_file="world_tool_file",
        )
    )
    prompt_file = provider.get_prompt_file()
    assert prompt_file == "world_prompt_file"


def test_get_prompt_file_template_data_none():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    provider._get_template_type_data = Mock(return_value=None)
    with pytest.raises(ValueError) as exc_info:
        prompt_file = provider.get_prompt_file()
    assert (
        f"Failed to produce template data for father place identifier '{father_place_identifier}' and template type {template_type}."
        in str(exc_info)
    )


def test_get_prompt_kwargs():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    template_data = TemplateTypeData(
        prompt_file="world_prompt_file",
        father_templates_file_path="father_templates_file",
        current_place_templates_file_path="current_place_templates_file",
        tool_file="world_tool_file",
    )
    provider._get_template_type_data = Mock(return_value=template_data)
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
    prompt_kwargs = provider.get_prompt_kwargs()
    expected_prompt_kwargs = {
        "father_place_name": "some_father_place",
        "father_place_description": "Father place description",
        "father_place_categories": ["category1", "category2"],
        "current_place_type_names": ["place1", "place2"],
    }
    assert prompt_kwargs == expected_prompt_kwargs


def test_get_tool_file():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    template_data = TemplateTypeData(
        prompt_file="world_prompt_file",
        father_templates_file_path="father_templates_file",
        current_place_templates_file_path="current_place_templates_file",
        tool_file="world_tool_file",
    )
    provider._get_template_type_data = Mock(return_value=template_data)
    tool_file = provider.get_tool_file()
    assert tool_file == "world_tool_file"


def test_get_user_content_with_notion():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    user_content = provider.get_user_content()
    expected_content = "Create the name and description of a world, following the above instructions. User guidance about how he wants this place to be: some notion"
    assert user_content == expected_content


def test_create_product():
    produce_tool_response_strategy_factory = Mock()
    filesystem_manager = Mock()
    father_place_identifier = "some_father_place"
    template_type = TemplateType.WORLD
    notion = "some notion"
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )
    arguments = {"key": "value"}
    product = provider.create_product_from_dict(arguments)
    assert isinstance(product, ConcreteLlmToolResponseProduct)
    assert product.get() == arguments
    assert product.is_valid() == True
