from typing import List
from unittest.mock import Mock

import pytest

from src.base.products.text_product import TextProduct
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
# Import the classes to be tested
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager


@pytest.fixture
def filter_factory_mock():
    return Mock(spec=FilterPlacesByCategoriesAlgorithmFactory)


@pytest.fixture
def place_selection_manager_mock():
    return Mock(spec=PlaceSelectionManager)


@pytest.fixture
def factory_instance(filter_factory_mock, place_selection_manager_mock):
    return ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
        filter_places_by_categories_algorithm_factory=filter_factory_mock,
        place_selection_manager=place_selection_manager_mock,
        place_type="park",
    )


def test_create_place_with_empty_categories(factory_instance):
    place_templates = {"template1": "Place A", "template2": "Place B"}
    categories: List[str] = []

    with pytest.raises(ValueError) as exc_info:
        factory_instance.create_place(place_templates, categories)

    assert (
        str(exc_info.value)
        == "Attempted to create a random place, but failed to pass the categories."
    )


def test_create_place_with_no_filtered_places(factory_instance, filter_factory_mock):
    place_templates = {"template1": "Place A", "template2": "Place B"}
    categories = ["nature", "recreation"]

    # Mock the algorithm to return an empty list
    algorithm_mock = Mock()
    algorithm_mock.do_algorithm.return_value = []
    filter_factory_mock.create_algorithm.return_value = algorithm_mock

    result = factory_instance.create_place(place_templates, categories)

    assert isinstance(result, TextProduct)
    assert not result.is_valid()
    expected_error = "No available templates for the selected type in this 'park'."
    assert result.get_error() == expected_error
    assert result.get() is None

    # Ensure the algorithm was called correctly
    filter_factory_mock.create_algorithm.assert_called_once_with(
        place_templates, categories
    )
    algorithm_mock.do_algorithm.assert_called_once()


def test_create_place_with_filtered_places(
    factory_instance, filter_factory_mock, place_selection_manager_mock
):
    place_templates = {"template1": "Place A", "template2": "Place B"}
    categories = ["nature", "recreation"]
    filtered_places = ["Place A"]

    # Mock the algorithm to return filtered_places
    algorithm_mock = Mock()
    algorithm_mock.do_algorithm.return_value = filtered_places
    filter_factory_mock.create_algorithm.return_value = algorithm_mock

    # Mock the place selection manager to return a specific place
    place_selection_manager_mock.select_random_place.return_value = "Place A"

    result = factory_instance.create_place(place_templates, categories)

    assert isinstance(result, TextProduct)
    assert result.is_valid()
    assert result.get() == "Place A"
    assert result.get_error() is None

    # Ensure the algorithm was called correctly
    filter_factory_mock.create_algorithm.assert_called_once_with(
        place_templates, categories
    )
    algorithm_mock.do_algorithm.assert_called_once()

    # Ensure the place selection manager was called correctly
    place_selection_manager_mock.select_random_place.assert_called_once_with(
        filtered_places
    )


def test_create_place_with_none_place_type(
    factory_instance, filter_factory_mock, place_selection_manager_mock
):
    # Create an instance without specifying place_type
    factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
        filter_places_by_categories_algorithm_factory=filter_factory_mock,
        place_selection_manager=place_selection_manager_mock,
        place_type=None,
    )

    place_templates = {"template1": "Place A"}
    categories = ["culture"]

    # Mock the algorithm to return filtered_places
    filtered_places = ["Place A"]
    algorithm_mock = Mock()
    algorithm_mock.do_algorithm.return_value = filtered_places
    filter_factory_mock.create_algorithm.return_value = algorithm_mock

    # Mock the place selection manager to return a specific place
    place_selection_manager_mock.select_random_place.return_value = "Place A"

    result = factory.create_place(place_templates, categories)

    assert isinstance(result, TextProduct)
    assert result.is_valid()
    assert result.get() == "Place A"
    assert result.get_error() is None

    # Check the error message when filtered_places is empty with None place_type
    # To cover this, let's create another test case where filtered_places is empty

    # Mock the algorithm to return empty list
    algorithm_mock.do_algorithm.return_value = []
    result_invalid = factory.create_place(place_templates, categories)

    assert isinstance(result_invalid, TextProduct)
    assert not result_invalid.is_valid()
    expected_error = "No available templates."
    assert result_invalid.get_error() == expected_error
    assert result_invalid.get() is None


def test_create_place_with_empty_place_templates(factory_instance, filter_factory_mock):
    place_templates = {}
    categories = ["nature"]

    # Mock the algorithm to return empty list since place_templates is empty
    algorithm_mock = Mock()
    algorithm_mock.do_algorithm.return_value = []
    filter_factory_mock.create_algorithm.return_value = algorithm_mock

    result = factory_instance.create_place(place_templates, categories)

    assert isinstance(result, TextProduct)
    assert not result.is_valid()
    expected_error = "No available templates for the selected type in this 'park'."
    assert result.get_error() == expected_error
    assert result.get() is None


@pytest.mark.parametrize(
    "place_type, expected_error",
    [
        ("museum", "No available templates for the selected type in this 'museum'."),
        ("beach", "No available templates for the selected type in this 'beach'."),
        (None, "No available templates."),
    ],
)
def test_error_message_with_various_place_types(
    place_type, expected_error, filter_factory_mock, place_selection_manager_mock
):
    factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
        filter_places_by_categories_algorithm_factory=filter_factory_mock,
        place_selection_manager=place_selection_manager_mock,
        place_type=place_type,
    )

    place_templates = {"template1": "Place A"}
    categories = ["history"]

    # Mock the algorithm to return empty list
    algorithm_mock = Mock()
    algorithm_mock.do_algorithm.return_value = []
    filter_factory_mock.create_algorithm.return_value = algorithm_mock

    result = factory.create_place(place_templates, categories)

    assert isinstance(result, TextProduct)
    assert not result.is_valid()
    assert result.get_error() == expected_error
    assert result.get() is None
