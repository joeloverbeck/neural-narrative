# test_concrete_filtered_place_description_generation_factory.py
from typing import cast
from unittest.mock import MagicMock

from pydantic import BaseModel

from src.maps.configs.filtered_place_description_generation_factory_config import (
    FilteredPlaceDescriptionGenerationFactoryConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_factories_config import (
    FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
)
from src.maps.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
from src.maps.models.area import Area
from src.maps.models.place_description import PlaceDescription
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_filtered_place_description_generation_product import (
    ConcreteFilteredPlaceDescriptionGenerationProduct,
)

# Mock constants
PLACE_DESCRIPTION_PROMPT_FILE = "place_description_prompt.txt"
TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE = "tool_instructions_for_instructor.txt"


# Begin tests
def test_get_tool_data():
    config = FilteredPlaceDescriptionGenerationFactoryConfig(
        playthrough_name="test_playthrough", place_identifier="test_place"
    )
    factories_config = MagicMock()
    factory = ConcreteFilteredPlaceDescriptionGenerationFactory(
        config=config, factories_config=factories_config
    )
    result = factory._get_tool_data(PlaceDescription)
    assert result == PlaceDescription.model_json_schema()


def test_get_user_content():
    config = FilteredPlaceDescriptionGenerationFactoryConfig(
        playthrough_name="test_playthrough", place_identifier="test_place"
    )
    factories_config = MagicMock()
    factory = ConcreteFilteredPlaceDescriptionGenerationFactory(
        config=config, factories_config=factories_config
    )
    result = factory.get_user_content()
    expected = "Write the description of the indicated place, filtered through the perspective of the character whose data has been provided, as per the above instructions."
    assert result == expected


def test_create_product_from_base_model():
    config = FilteredPlaceDescriptionGenerationFactoryConfig(
        playthrough_name="test_playthrough", place_identifier="test_place"
    )
    factories_config = MagicMock()
    factory = ConcreteFilteredPlaceDescriptionGenerationFactory(
        config=config, factories_config=factories_config
    )

    class MockBaseModel(BaseModel):
        description: str

    base_model = MockBaseModel(description="A beautiful place.")
    product = factory.create_product_from_base_model(base_model)
    assert isinstance(product, ConcreteFilteredPlaceDescriptionGenerationProduct)
    assert product.get() == "A beautiful place."
    assert product.is_valid() == True


def test_get_prompt_kwargs():
    config = FilteredPlaceDescriptionGenerationFactoryConfig(
        playthrough_name="test_playthrough", place_identifier="test_place"
    )

    # Mock dependencies
    produce_tool_response_strategy_factory = MagicMock()
    character_information_factory = MagicMock()
    place_manager_factory = MagicMock()
    map_manager_factory = MagicMock()
    weathers_manager = MagicMock()

    factories_config = FilteredPlaceDescriptionGenerationFactoryFactoriesConfig(
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        character_information_factory=character_information_factory,
        place_manager_factory=place_manager_factory,
        map_manager_factory=map_manager_factory,
        weathers_manager=weathers_manager,
    )

    time_manager = MagicMock()
    time_manager.get_hour.return_value = 12
    time_manager.get_time_of_the_day.return_value = "noon"

    filesystem_manager = MagicMock()

    factory = ConcreteFilteredPlaceDescriptionGenerationFactory(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        time_manager=time_manager,
    )

    # Mock method calls
    place_type = MagicMock()
    place_type.value = "city"

    place_manager = MagicMock()
    place_manager.determine_place_type.return_value = place_type
    place_manager_factory.create_place_manager.return_value = place_manager

    place_full_data = {
        "city_data": {
            "name": "Test City",
            "description": "A bustling metropolis.",
        }
    }

    map_manager = MagicMock()
    map_manager.get_place_full_data.return_value = place_full_data
    map_manager_factory.create_map_manager.return_value = map_manager

    weathers_manager.get_current_weather_identifier.return_value = "sunny"
    weathers_manager.get_weather_description.return_value = "A bright sunny day."

    character_information_factory.get_information.return_value = "Test character info"

    result = factory.get_prompt_kwargs()

    expected = {
        "hour": 12,
        "time_of_the_day": "noon",
        "weather": "A bright sunny day.",
        "place_type": "city",
        "place_template": "Test City",
        "place_description": "A bustling metropolis.",
        "character_information": "Test character info",
    }

    assert result == expected


def test_generate_product():
    config = FilteredPlaceDescriptionGenerationFactoryConfig(
        playthrough_name="test_playthrough", place_identifier="test_place"
    )

    # Mock dependencies
    produce_tool_response_strategy_factory = MagicMock()
    character_information_factory = MagicMock()
    place_manager_factory = MagicMock()
    map_manager_factory = MagicMock()
    weathers_manager = MagicMock()

    factories_config = FilteredPlaceDescriptionGenerationFactoryFactoriesConfig(
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        character_information_factory=character_information_factory,
        place_manager_factory=place_manager_factory,
        map_manager_factory=map_manager_factory,
        weathers_manager=weathers_manager,
    )

    time_manager = MagicMock()
    time_manager.get_hour.return_value = 12
    time_manager.get_time_of_the_day.return_value = "noon"

    filesystem_manager = MagicMock()
    filesystem_manager.read_file.side_effect = lambda x: f"Content of {x}"

    factory = ConcreteFilteredPlaceDescriptionGenerationFactory(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
        time_manager=time_manager,
    )

    # Mock method calls
    place_type = MagicMock()
    place_type.value = "city"

    place_manager = MagicMock()
    place_manager.determine_place_type.return_value = place_type
    place_manager_factory.create_place_manager.return_value = place_manager

    place_full_data = {
        "city_data": {
            "name": "Test City",
            "description": "A bustling metropolis.",
        }
    }

    map_manager = MagicMock()
    map_manager.get_place_full_data.return_value = place_full_data
    map_manager_factory.create_map_manager.return_value = map_manager

    weathers_manager.get_current_weather_identifier.return_value = "sunny"
    weathers_manager.get_weather_description.return_value = "A bright sunny day."

    character_information_factory.get_information.return_value = "Test character info"

    # Mock strategy
    strategy = MagicMock()

    class MockBaseModel(BaseModel):
        description: str

    strategy.produce_tool_response.return_value = MockBaseModel(
        description="Generated description."
    )
    produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
        strategy
    )

    product = factory.generate_product(Area)

    assert isinstance(product, ConcreteFilteredPlaceDescriptionGenerationProduct)
    assert product.get() == "Generated description."
    assert product.is_valid() == True
