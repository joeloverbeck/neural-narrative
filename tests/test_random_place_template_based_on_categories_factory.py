from unittest.mock import MagicMock

import pytest

from src.base.required_string import RequiredString
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager


class TestConcreteRandomPlaceTemplateBasedOnCategoriesFactory:

    def test_create_random_place_template_with_matching_categories(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }

        categories = [RequiredString("food")]
        location_type = RequiredString("SomeLocationType")

        filtered_places = {
            "Place1": {"categories": ["food", "drink"]},
            "Place3": {"categories": ["food", "music"]},
        }

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = RequiredString(
            "Place1"
        )

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act
        result = factory.create_random_place_template_based_on_categories(
            place_templates, categories
        )

        # Assert
        assert result.is_valid() == True
        assert result.get() == RequiredString("Place1")
        assert result.get_error() is None

        mock_place_selection_manager.filter_places_by_categories.assert_called_once_with(
            place_templates, categories, location_type
        )
        mock_place_selection_manager.select_random_place.assert_called_once_with(
            filtered_places
        )

    def test_create_random_place_template_with_no_matching_categories(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }

        categories = [RequiredString("sports")]
        location_type = RequiredString("SomeLocationType")

        filtered_places = {}

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act
        result = factory.create_random_place_template_based_on_categories(
            place_templates, categories
        )

        # Assert
        assert result.is_valid() == False
        assert result.get() is None
        assert (
            result.get_error()
            == "No available templates for the selected type in this area."
        )

        mock_place_selection_manager.filter_places_by_categories.assert_called_once_with(
            place_templates, categories, location_type
        )
        mock_place_selection_manager.select_random_place.assert_called_once_with(
            filtered_places
        )

    def test_create_random_place_template_with_empty_place_templates(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {}
        categories = [RequiredString("food")]
        location_type = RequiredString("SomeLocationType")

        filtered_places = {}

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act
        result = factory.create_random_place_template_based_on_categories(
            place_templates, categories
        )

        # Assert
        assert result.is_valid() == False
        assert result.get() is None
        assert (
            result.get_error()
            == "No available templates for the selected type in this area."
        )

    def test_create_random_place_template_with_empty_categories(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }

        categories = []  # Empty categories list
        location_type = RequiredString("SomeLocationType")

        filtered_places = place_templates.copy()

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = RequiredString(
            "Place2"
        )

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            factory.create_random_place_template_based_on_categories(
                place_templates, categories
            )

        assert "Attempted to create a random place" in str(exc_info.value)

    def test_create_random_place_template_with_none_location_type(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }

        categories = [RequiredString("music")]

        location_type = None

        filtered_places = {
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = RequiredString(
            "Place3"
        )

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act
        result = factory.create_random_place_template_based_on_categories(
            place_templates, categories
        )

        # Assert
        assert result.is_valid() == True
        assert result.get() == RequiredString("Place3")
        assert result.get_error() is None

    def test_create_random_place_template_select_random_place_returns_none(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["food", "entertainment"]},
        }

        categories = [RequiredString("food")]
        location_type = RequiredString("SomeLocationType")

        filtered_places = place_templates

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act
        result = factory.create_random_place_template_based_on_categories(
            place_templates, categories
        )

        # Assert
        assert result.is_valid() == False
        assert result.get() is None
        assert (
            result.get_error()
            == "No available templates for the selected type in this area."
        )

    def test_create_random_place_template_exception_in_filter_places_by_categories(
        self,
    ):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
        }

        categories = [RequiredString("food")]
        location_type = RequiredString("SomeLocationType")

        def filter_places_by_categories_side_effect(*args, **kwargs):
            raise Exception("Error during filtering")

        mock_place_selection_manager.filter_places_by_categories.side_effect = (
            filter_places_by_categories_side_effect
        )

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act and Assert
        with pytest.raises(Exception) as exc_info:
            factory.create_random_place_template_based_on_categories(
                place_templates, categories
            )

        assert str(exc_info.value) == "Error during filtering"

    def test_create_random_place_template_exception_in_select_random_place(self):
        # Arrange
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)

        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
        }

        categories = [RequiredString("food")]
        location_type = RequiredString("SomeLocationType")

        filtered_places = place_templates

        mock_place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )

        def select_random_place_side_effect(*args, **kwargs):
            raise Exception("Error during random selection")

        mock_place_selection_manager.select_random_place.side_effect = (
            select_random_place_side_effect
        )

        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )

        # Act and Assert
        with pytest.raises(Exception) as exc_info:
            factory.create_random_place_template_based_on_categories(
                place_templates, categories
            )

        assert str(exc_info.value) == "Error during random selection"
