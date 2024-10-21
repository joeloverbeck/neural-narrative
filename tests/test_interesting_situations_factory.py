from unittest.mock import Mock

import pytest

from src.base.required_string import RequiredString
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.concepts.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


# Fixture for mocking dependencies
@pytest.fixture
def mock_dependencies():
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    places_descriptions_factory = Mock(spec=PlacesDescriptionsProvider)
    player_and_followers_information_factory = Mock(
        spec=PlayerAndFollowersInformationFactory
    )
    filesystem_manager = Mock(spec=FilesystemManager)
    return {
        "produce_tool_response_strategy_factory": produce_tool_response_strategy_factory,
        "places_descriptions_factory": places_descriptions_factory,
        "player_and_followers_information_factory": player_and_followers_information_factory,
        "filesystem_manager": filesystem_manager,
    }


# Test create_product Success
def test_create_product_success(mock_dependencies):
    factory = InterestingSituationsFactory(
        playthrough_name=RequiredString("TestPlaythrough"),
        produce_tool_response_strategy_factory=mock_dependencies[
            "produce_tool_response_strategy_factory"
        ],
        places_descriptions_factory=mock_dependencies["places_descriptions_factory"],
        player_and_followers_information_factory=mock_dependencies[
            "player_and_followers_information_factory"
        ],
        filesystem_manager=mock_dependencies["filesystem_manager"],
    )

    arguments = {
        "interesting_situation_1": "A mysterious stranger arrives in town.",
        "interesting_situation_2": "A hidden treasure map is discovered.",
        "interesting_situation_3": "An ancient curse is unleashed.",
    }

    product = factory.create_product(arguments)

    assert isinstance(product, InterestingSituationsProduct)
    assert product.is_valid() == True
    assert len(product.get()) == 3
    assert product.get()[0].value == "A mysterious stranger arrives in town."
    assert product.get()[1].value == "A hidden treasure map is discovered."
    assert product.get()[2].value == "An ancient curse is unleashed."
    assert product.error() is None


# Test create_product with Missing Keys
@pytest.mark.parametrize(
    "missing_key",
    ["interesting_situation_1", "interesting_situation_2", "interesting_situation_3"],
)
def test_create_product_missing_keys(mock_dependencies, missing_key):
    factory = InterestingSituationsFactory(
        playthrough_name=RequiredString("TestPlaythrough"),
        produce_tool_response_strategy_factory=mock_dependencies[
            "produce_tool_response_strategy_factory"
        ],
        places_descriptions_factory=mock_dependencies["places_descriptions_factory"],
        player_and_followers_information_factory=mock_dependencies[
            "player_and_followers_information_factory"
        ],
        filesystem_manager=mock_dependencies["filesystem_manager"],
    )

    arguments = {
        "interesting_situation_1": "A mysterious stranger arrives in town.",
        "interesting_situation_2": "A hidden treasure map is discovered.",
        "interesting_situation_3": "An ancient curse is unleashed.",
    }

    # Remove one key
    del arguments[missing_key]

    with pytest.raises(ValueError) as exc_info:
        factory.create_product(arguments)

    assert str(exc_info.value) == "value can't be empty."


# Test create_product with Empty Values
@pytest.mark.parametrize(
    "empty_key",
    ["interesting_situation_1", "interesting_situation_2", "interesting_situation_3"],
)
def test_create_product_empty_values(mock_dependencies, empty_key):
    factory = InterestingSituationsFactory(
        playthrough_name=RequiredString("TestPlaythrough"),
        produce_tool_response_strategy_factory=mock_dependencies[
            "produce_tool_response_strategy_factory"
        ],
        places_descriptions_factory=mock_dependencies["places_descriptions_factory"],
        player_and_followers_information_factory=mock_dependencies[
            "player_and_followers_information_factory"
        ],
        filesystem_manager=mock_dependencies["filesystem_manager"],
    )

    arguments = {
        "interesting_situation_1": "A mysterious stranger arrives in town.",
        "interesting_situation_2": "A hidden treasure map is discovered.",
        "interesting_situation_3": "An ancient curse is unleashed.",
        empty_key: "",
    }

    # Set one key to empty string

    with pytest.raises(ValueError) as exc_info:
        factory.create_product(arguments)

    assert str(exc_info.value) == "value can't be empty."


# Test create_product with Invalid Types
@pytest.mark.parametrize(
    "invalid_value", [123, None, ["List"], {"key": "value"}, 45.67]
)
def test_create_product_invalid_types(mock_dependencies, invalid_value):
    factory = InterestingSituationsFactory(
        playthrough_name=RequiredString("TestPlaythrough"),
        produce_tool_response_strategy_factory=mock_dependencies[
            "produce_tool_response_strategy_factory"
        ],
        places_descriptions_factory=mock_dependencies["places_descriptions_factory"],
        player_and_followers_information_factory=mock_dependencies[
            "player_and_followers_information_factory"
        ],
        filesystem_manager=mock_dependencies["filesystem_manager"],
    )

    arguments = {
        "interesting_situation_1": invalid_value,
        "interesting_situation_2": "A hidden treasure map is discovered.",
        "interesting_situation_3": "An ancient curse is unleashed.",
    }

    # Set one key to invalid type

    if invalid_value is None or invalid_value == "":
        with pytest.raises(ValueError) as exc_info:
            factory.create_product(arguments)
        assert str(exc_info.value) == "value can't be empty."
    else:
        with pytest.raises(TypeError) as exc_info:
            factory.create_product(arguments)
        assert str(exc_info.value) == "value must be a string"
