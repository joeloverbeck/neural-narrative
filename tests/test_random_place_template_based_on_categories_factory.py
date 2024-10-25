from unittest.mock import MagicMock

import pytest

from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager


class TestConcreteRandomPlaceTemplateBasedOnCategoriesFactory:

    def test_create_random_place_template_with_matching_categories(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }
        categories = ["food"]
        location_type = "SomeLocationType"
        filtered_places = {
            "Place1": {"categories": ["food", "drink"]},
            "Place3": {"categories": ["food", "music"]},
        }
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = "Place1"
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        result = factory.create_place(place_templates, categories)
        assert result.is_valid() == True
        assert result.get() == "Place1"
        assert result.get_error() is None
        mock_place_selection_manager.filter_places_by_categories.assert_called_once_with(
            place_templates, categories, location_type
        )
        mock_place_selection_manager.select_random_place.assert_called_once_with(
            filtered_places
        )

    def test_create_random_place_template_with_no_matching_categories(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }
        categories = ["sports"]
        location_type = "SomeLocationType"
        filtered_places = {}
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        result = factory.create_place(place_templates, categories)
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
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {}
        categories = ["food"]
        location_type = "SomeLocationType"
        filtered_places = {}
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        result = factory.create_place(place_templates, categories)
        assert result.is_valid() == False
        assert result.get() is None
        assert (
            result.get_error()
            == "No available templates for the selected type in this area."
        )

    def test_create_random_place_template_with_empty_categories(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }
        categories = []
        location_type = "SomeLocationType"
        filtered_places = place_templates.copy()
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = "Place2"
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        with pytest.raises(Exception) as exc_info:
            factory.create_place(place_templates, categories)
        assert "Attempted to create a random place" in str(exc_info)

    def test_create_random_place_template_with_none_location_type(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }
        categories = ["music"]
        location_type = None
        filtered_places = {
            "Place2": {"categories": ["entertainment", "music"]},
            "Place3": {"categories": ["food", "music"]},
        }
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = "Place3"
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        result = factory.create_place(place_templates, categories)
        assert result.is_valid() == True
        assert result.get() == "Place3"
        assert result.get_error() is None

    def test_create_random_place_template_select_random_place_returns_none(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["food", "entertainment"]},
        }
        categories = ["food"]
        location_type = "SomeLocationType"
        filtered_places = place_templates
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
            filtered_places
        )
        mock_place_selection_manager.select_random_place.return_value = None
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        result = factory.create_place(place_templates, categories)
        assert result.is_valid() == False
        assert result.get() is None
        assert (
            result.get_error()
            == "No available templates for the selected type in this area."
        )

    def test_create_random_place_template_exception_in_filter_places_by_categories(
        self,
    ):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {
            "Place1": {"categories": ["food", "drink"]},
            "Place2": {"categories": ["entertainment", "music"]},
        }
        categories = ["food"]
        location_type = "SomeLocationType"

        def filter_places_by_categories_side_effect(*args, **kwargs):
            raise Exception("Error during filtering")

        (mock_place_selection_manager.filter_places_by_categories.side_effect) = (
            filter_places_by_categories_side_effect
        )
        factory = ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
            place_selection_manager=mock_place_selection_manager,
            location_type=location_type,
        )
        with pytest.raises(Exception) as exc_info:
            factory.create_place(place_templates, categories)
        assert "Error during filtering" in str(exc_info)

    def test_create_random_place_template_exception_in_select_random_place(self):
        mock_place_selection_manager = MagicMock(spec=PlaceSelectionManager)
        place_templates = {"Place1": {"categories": ["food", "drink"]}}
        categories = ["food"]
        location_type = "SomeLocationType"
        filtered_places = place_templates
        (mock_place_selection_manager.filter_places_by_categories.return_value) = (
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
        with pytest.raises(Exception) as exc_info:
            factory.create_place(place_templates, categories)
        assert "Error during random selection" in str(exc_info)
