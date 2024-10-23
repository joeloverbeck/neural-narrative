from typing import cast
from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


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
