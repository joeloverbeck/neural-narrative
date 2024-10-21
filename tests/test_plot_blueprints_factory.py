# test_plot_blueprints_factory.py
from typing import cast
from unittest.mock import patch

import pytest

from src.base.required_string import RequiredString
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


# Mock classes for dependencies
class MockProduceToolResponseStrategyFactory:
    pass


class MockPlacesDescriptionsProvider:
    pass


class MockPlayerAndFollowersInformationFactory:
    pass


class MockFilesystemManager:
    pass


@pytest.fixture
def factory():
    playthrough_name = RequiredString("Test Playthrough")
    produce_tool_response_strategy_factory = MockProduceToolResponseStrategyFactory()
    places_descriptions_factory = MockPlacesDescriptionsProvider()
    player_and_followers_information_factory = (
        MockPlayerAndFollowersInformationFactory()
    )
    filesystem_manager = MockFilesystemManager()

    with patch(
        "src.concepts.factories.base_concept_factory.BaseConceptFactory.__init__",
        return_value=None,
    ):
        return PlotBlueprintsFactory(
            playthrough_name,
            cast(
                ProduceToolResponseStrategyFactory,
                produce_tool_response_strategy_factory,
            ),
            cast(PlacesDescriptionsProvider, places_descriptions_factory),
            cast(
                PlayerAndFollowersInformationFactory,
                player_and_followers_information_factory,
            ),
            cast(FilesystemManager, filesystem_manager),
        )


def test_create_product_with_valid_plot_blueprint(factory):
    arguments = {
        "plot_blueprint": "This is a test plot blueprint.\nIt has multiple lines.\n\nAnd paragraphs."
    }
    product = factory.create_product(arguments)

    expected_plot_blueprint = (
        "This is a test plot blueprint. It has multiple lines. And paragraphs."
    )
    assert product.is_valid() == True
    assert product.get_error() is None
    assert product.get() == [RequiredString(expected_plot_blueprint)]


def test_create_product_with_missing_plot_blueprint(factory):
    arguments = {}
    product = factory.create_product(arguments)

    assert product.is_valid() == False
    assert product.get_error() == "The LLM failed to produce a plot blueprint."
    assert product.get() is None


def test_create_product_with_empty_plot_blueprint(factory):
    arguments = {"plot_blueprint": ""}
    product = factory.create_product(arguments)

    assert product.is_valid() == False
    assert product.get_error() == "The LLM failed to produce a plot blueprint."
    assert product.get() is None


def test_create_product_with_newlines_in_plot_blueprint(factory):
    arguments = {"plot_blueprint": "First line.\nSecond line.\n\nThird paragraph."}
    product = factory.create_product(arguments)

    expected_plot_blueprint = "First line. Second line. Third paragraph."
    assert product.is_valid() == True
    assert product.get_error() is None
    assert product.get() == [RequiredString(expected_plot_blueprint)]


def test_create_product_with_non_string_plot_blueprint(factory):
    arguments = {"plot_blueprint": 123}
    product = factory.create_product(arguments)

    expected_plot_blueprint = "123"
    assert product.is_valid() == True
    assert product.get_error() is None
    assert product.get() == [RequiredString(expected_plot_blueprint)]


def test_create_product_with_none_plot_blueprint(factory):
    arguments = {"plot_blueprint": None}
    product = factory.create_product(arguments)

    assert product.is_valid() == False
    assert product.get_error() == "The LLM failed to produce a plot blueprint."
    assert product.get() is None


def test_create_product_with_whitespace_plot_blueprint(factory):
    arguments = {"plot_blueprint": "   \n   \n"}
    product = factory.create_product(arguments)

    assert product.is_valid() == False
    assert product.get_error() == "The LLM failed to produce a plot blueprint."
    assert product.get() is None
