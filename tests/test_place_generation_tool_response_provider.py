from typing import cast
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel

from src.base.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.maps.models.area import Area
from src.maps.models.region import Region
from src.maps.models.world import World
from src.maps.templates_repository import TemplatesRepository
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


# test_place_generation_tool_response_provider.py


# Mock models and constants
class MockWorld(BaseModel):
    name: str
    description: str


class MockRegion(BaseModel):
    name: str
    description: str


class MockArea(BaseModel):
    name: str
    description: str


class MockLocation(BaseModel):
    name: str
    description: str
    type: str


# Mock functions
def mock_validate_non_empty_string(value, field_name):
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")


def mock_get_custom_location_class():
    return MockLocation


def test_init_valid_arguments():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.WORLD
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)
    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
    )

    assert provider._father_place_identifier == father_place_identifier
    assert provider._template_type == template_type
    assert provider._notion == notion
    assert (
        provider._produce_tool_response_strategy_factory
        == produce_tool_response_strategy_factory
    )
    assert provider._templates_repository == templates_repository


def test_init_empty_father_place_identifier():
    father_place_identifier = ""
    template_type = TemplateType.WORLD
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)

    with pytest.raises(ValueError) as excinfo:
        PlaceGenerationToolResponseProvider(
            father_place_identifier,
            template_type,
            notion,
            cast(
                ProduceToolResponseStrategyFactory,
                produce_tool_response_strategy_factory,
            ),
            templates_repository,
        )
    assert "'father_place_identifier' must be a" in str(excinfo.value)


def test_get_template_type_data():
    father_place_identifier = "SomePlaceIdentifier"
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)

    # Test for each TemplateType
    for template_type in TemplateType:
        provider = PlaceGenerationToolResponseProvider(
            father_place_identifier,
            template_type,
            notion,
            cast(
                ProduceToolResponseStrategyFactory,
                produce_tool_response_strategy_factory,
            ),
            templates_repository,
        )
        template_data = provider._get_template_type_data()

        path_manager = PathManager()

        if template_type == TemplateType.WORLD:
            assert (
                template_data.prompt_file
                == path_manager.get_world_generation_prompt_path()
            )
            assert template_data.response_model == World
        elif template_type == TemplateType.REGION:
            assert (
                template_data.prompt_file
                == path_manager.get_region_generation_prompt_path()
            )
            assert template_data.response_model == Region
        elif template_type == TemplateType.AREA:
            assert (
                template_data.prompt_file
                == path_manager.get_area_generation_prompt_path()
            )
            assert template_data.response_model == Area
        elif template_type == TemplateType.LOCATION:
            assert (
                template_data.prompt_file
                == path_manager.get_location_generation_prompt_path()
            )
        elif template_type == TemplateType.ROOM:
            assert (
                template_data.prompt_file
                == path_manager.get_room_generation_prompt_path()
            )
        else:
            assert template_data is None


def test_get_prompt_file_valid():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.WORLD
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
    )

    prompt_file = provider.get_prompt_file()

    path_manager = PathManager()
    assert prompt_file == path_manager.get_world_generation_prompt_path()


def test_get_prompt_kwargs():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.REGION
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )

    # Mock templates_repository to return specific templates
    templates_repository = Mock(spec=TemplatesRepository)
    parent_template = {
        "description": "Parent description",
        "categories": ["Category1", "Category2"],
    }
    current_place_type_templates = {"Place1": {}, "Place2": {}}

    templates_repository.load_templates.side_effect = [
        {father_place_identifier: parent_template},  # First call
        current_place_type_templates,  # Second call
    ]

    filesystem_manager = Mock(spec=FilesystemManager)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
        filesystem_manager,
    )

    prompt_kwargs = provider.get_prompt_kwargs()

    assert prompt_kwargs["father_place_name"] == father_place_identifier
    assert prompt_kwargs["father_place_description"] == "Parent description"
    assert prompt_kwargs["father_place_categories"] == ["Category1", "Category2"]
    assert prompt_kwargs["current_place_type_names"] == ["Place1", "Place2"]


def test_get_user_content_with_notion():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.AREA
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)
    filesystem_manager = Mock(spec=FilesystemManager)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
        filesystem_manager,
    )

    user_content = provider.get_user_content()
    expected_content = (
        f"Create the name and description of a {template_type.value}, following the above instructions."
        f" User guidance about how he wants this place to be: {notion}"
    )
    assert user_content == expected_content


def test_get_user_content_without_notion():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.AREA
    notion = ""
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)
    filesystem_manager = Mock(spec=FilesystemManager)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
        filesystem_manager,
    )

    user_content = provider.get_user_content()
    expected_content = f"Create the name and description of a {template_type.value}, following the above instructions."
    assert user_content == expected_content


def test_create_product_from_base_model_non_location():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.AREA
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)
    filesystem_manager = Mock(spec=FilesystemManager)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
        filesystem_manager,
    )

    response_model = MockArea(name="AreaName", description="AreaDescription")

    product = provider.create_product_from_base_model(response_model)

    assert product.get()["name"] == "AreaName"
    assert product.get()["description"] == "AreaDescription"
    assert "type" not in product.get()
    assert product.is_valid() == True


def test_create_product_from_base_model_location():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.LOCATION
    notion = "Some notion"
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    templates_repository = Mock(spec=TemplatesRepository)
    filesystem_manager = Mock(spec=FilesystemManager)

    provider = PlaceGenerationToolResponseProvider(
        father_place_identifier,
        template_type,
        notion,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        templates_repository,
        filesystem_manager,
    )

    response_model = MockLocation(
        name="LocationName", description="LocationDescription", type="LocationType"
    )

    product = provider.create_product_from_base_model(response_model)

    assert product.get()["name"] == "LocationName"
    assert product.get()["description"] == "LocationDescription"
    assert product.get()["type"] == "LocationType"
    assert product.is_valid() == True


def test_generate_product():
    father_place_identifier = "SomePlaceIdentifier"
    template_type = TemplateType.WORLD
    notion = "Some notion"

    # Mock dependencies
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    strategy = Mock()
    produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
        strategy
    )
    templates_repository = Mock(spec=TemplatesRepository)
    templates_repository.load_templates.side_effect = [
        {father_place_identifier: {"description": "Desc", "categories": []}},
        {"Place1": {}, "Place2": {}},
    ]

    # Mock BaseToolResponseProvider methods
    with patch.object(
        PlaceGenerationToolResponseProvider,
        "_read_prompt_file",
        return_value="Prompt template",
    ):
        with patch.object(
            PlaceGenerationToolResponseProvider,
            "_read_tool_instructions",
            return_value="Tool instructions",
        ):
            provider = PlaceGenerationToolResponseProvider(
                father_place_identifier,
                template_type,
                notion,
                cast(
                    ProduceToolResponseStrategyFactory,
                    produce_tool_response_strategy_factory,
                ),
                templates_repository,
            )

            # Mock response_model
            response_model = MockWorld(name="WorldName", description="WorldDescription")

            # Mock strategy.produce_tool_response to return response_model
            strategy.produce_tool_response.return_value = response_model

            product = provider.generate_product(MockWorld)

            # Assertions
            assert product.get()["name"] == "WorldName"
            assert product.get()["description"] == "WorldDescription"
            assert product.is_valid() == True

            # Ensure that produce_tool_response was called with correct arguments
            strategy.produce_tool_response.assert_called_once()


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
        provider.get_prompt_file()
    assert (
        f"Failed to produce template data for father place identifier '{father_place_identifier}' and template type {template_type}."
        in str(exc_info)
    )
