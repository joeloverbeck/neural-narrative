from unittest.mock import MagicMock, patch

import pytest

from src.maps.place_selection_manager import PlaceSelectionManager


# Since we don't have actual implementations of PlaceManagerFactory and TemplatesRepository,
# we'll mock them.


def test_get_available_location_types():
    # Arrange
    place_categories = ["forest", "mountain"]
    location_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
        "place3": {"categories": ["desert"], "type": "oasis"},
        "place4": {"categories": ["forest"], "type": "grove"},
    }
    used_templates = ["place2"]

    # Mock the dependencies
    place_manager = MagicMock()
    place_manager.get_place_categories.return_value = place_categories
    place_manager.get_places_of_type.return_value = used_templates

    place_manager_factory = MagicMock()
    place_manager_factory.create_place_manager.return_value = place_manager

    template_repository = MagicMock()
    template_repository.load_template.return_value = location_templates

    manager = PlaceSelectionManager(place_manager_factory, template_repository)

    current_area_template = "some_area_template"

    # Act
    available_location_types = manager.get_available_location_types(
        current_area_template
    )

    # Assert
    expected_types = [
        "cave",
        "grove",
    ]  # place1 and place4 match categories and are not used
    assert set(available_location_types) == set(expected_types)


def test_get_available_location_types_no_matching_places():
    # Arrange
    place_categories = ["ocean"]
    location_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
    }
    used_templates = []

    # Mock the dependencies
    place_manager = MagicMock()
    place_manager.get_place_categories.return_value = place_categories
    place_manager.get_places_of_type.return_value = used_templates

    place_manager_factory = MagicMock()
    place_manager_factory.create_place_manager.return_value = place_manager

    template_repository = MagicMock()
    template_repository.load_template.return_value = location_templates

    manager = PlaceSelectionManager(place_manager_factory, template_repository)

    current_area_template = "some_area_template"

    # Act
    available_location_types = manager.get_available_location_types(
        current_area_template
    )

    # Assert
    assert available_location_types == []


def test_get_available_location_types_all_used():
    # Arrange
    place_categories = ["forest", "mountain"]
    location_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
    }
    used_templates = ["place1", "place2"]

    # Mock the dependencies
    place_manager = MagicMock()
    place_manager.get_place_categories.return_value = place_categories
    place_manager.get_places_of_type.return_value = used_templates

    place_manager_factory = MagicMock()
    place_manager_factory.create_place_manager.return_value = place_manager

    template_repository = MagicMock()
    template_repository.load_template.return_value = location_templates

    manager = PlaceSelectionManager(place_manager_factory, template_repository)

    current_area_template = "some_area_template"

    # Act
    available_location_types = manager.get_available_location_types(
        current_area_template
    )

    # Assert
    assert available_location_types == []


def test_get_available_location_types_no_templates():
    # Arrange
    place_categories = ["forest", "mountain"]
    location_templates = {}
    used_templates = []

    # Mock the dependencies
    place_manager = MagicMock()
    place_manager.get_place_categories.return_value = place_categories
    place_manager.get_places_of_type.return_value = used_templates

    place_manager_factory = MagicMock()
    place_manager_factory.create_place_manager.return_value = place_manager

    template_repository = MagicMock()
    template_repository.load_template.return_value = location_templates

    manager = PlaceSelectionManager(place_manager_factory, template_repository)

    current_area_template = "some_area_template"

    # Act
    available_location_types = manager.get_available_location_types(
        current_area_template
    )

    # Assert
    assert available_location_types == []


def test_get_available_location_types_no_place_categories():
    # Arrange
    place_categories = []
    location_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
    }
    used_templates = []

    # Mock the dependencies
    place_manager = MagicMock()
    place_manager.get_place_categories.return_value = place_categories
    place_manager.get_places_of_type.return_value = used_templates

    place_manager_factory = MagicMock()
    place_manager_factory.create_place_manager.return_value = place_manager

    template_repository = MagicMock()
    template_repository.load_template.return_value = location_templates

    manager = PlaceSelectionManager(place_manager_factory, template_repository)

    current_area_template = "some_area_template"

    # Act
    available_location_types = manager.get_available_location_types(
        current_area_template
    )

    # Assert
    assert available_location_types == []


def test_filter_places_by_categories_no_location_type():
    place_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
        "place3": {"categories": ["desert"], "type": "oasis"},
        "place4": {"categories": ["forest"], "type": "grove"},
    }
    father_place_categories = ["forest", "mountain"]

    expected_filtered_places = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
        "place4": {"categories": ["forest"], "type": "grove"},
    }

    filtered_places = PlaceSelectionManager.filter_places_by_categories(
        place_templates, father_place_categories
    )

    assert filtered_places == expected_filtered_places


def test_filter_places_by_categories_with_location_type():
    place_templates = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
        "place3": {"categories": ["desert"], "type": "oasis"},
        "place4": {"categories": ["forest"], "type": "grove"},
    }
    father_place_categories = ["forest", "mountain"]
    location_type = "cave"

    expected_filtered_places = {
        "place1": {"categories": ["forest"], "type": "cave"},
    }

    filtered_places = PlaceSelectionManager.filter_places_by_categories(
        place_templates, father_place_categories, location_type
    )

    assert filtered_places == expected_filtered_places


def test_filter_places_by_categories_no_matches():
    place_templates = {
        "place1": {"categories": ["desert"], "type": "oasis"},
        "place2": {"categories": ["ocean"], "type": "island"},
    }
    father_place_categories = ["forest", "mountain"]

    expected_filtered_places = {}

    filtered_places = PlaceSelectionManager.filter_places_by_categories(
        place_templates, father_place_categories
    )

    assert filtered_places == expected_filtered_places


def test_select_random_place_empty():
    matching_places = {}

    with pytest.raises(ValueError) as exc_info:
        PlaceSelectionManager.select_random_place(matching_places)

    assert (
            str(exc_info.value)
            == "No matching places found. Consider generating places of the desired type."
    )


def test_select_random_place_single_item():
    matching_places = {"place1": {"categories": ["forest"], "type": "cave"}}

    selected_place = PlaceSelectionManager.select_random_place(matching_places)

    assert selected_place == "place1"


def test_select_random_place_multiple_items():
    matching_places = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
        "place3": {"categories": ["desert"], "type": "oasis"},
    }

    selected_place = PlaceSelectionManager.select_random_place(matching_places)

    assert selected_place in matching_places.keys()


@patch("random.choice")
def test_select_random_place_mocked_random_choice(mock_choice):
    matching_places = {
        "place1": {"categories": ["forest"], "type": "cave"},
        "place2": {"categories": ["mountain"], "type": "peak"},
    }
    mock_choice.return_value = "place2"

    selected_place = PlaceSelectionManager.select_random_place(matching_places)

    assert selected_place == "place2"
