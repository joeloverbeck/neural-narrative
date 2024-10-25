from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.maps.templates_repository import TemplatesRepository


@pytest.fixture
def mock_map_repository():
    return Mock(spec=MapRepository)


@pytest.fixture
def mock_template_repository():
    return Mock(spec=TemplatesRepository)


@pytest.fixture
def mock_playthrough_manager():
    return Mock(spec=PlaythroughManager)


@pytest.fixture
def place_manager(
    mock_map_repository, mock_template_repository, mock_playthrough_manager
):
    playthrough_name = "test_playthrough"
    return PlaceManager(
        playthrough_name,
        mock_map_repository,
        mock_template_repository,
        playthrough_manager=mock_playthrough_manager,
    )


def test_get_place_success(place_manager, mock_map_repository):
    place_identifier = "place1"
    map_data = {
        "place1": {"id": "place1", "name": "Place One"},
        "place2": {"id": "place2", "name": "Place Two"},
    }
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.get_place(place_identifier)
    assert result == map_data["place1"]
    mock_map_repository.load_map_data.assert_called_once()


def test_get_place_not_found(place_manager, mock_map_repository):
    place_identifier = "nonexistent_place"
    map_data = {
        "place1": {"id": "place1", "name": "Place One"},
        "place2": {"id": "place2", "name": "Place Two"},
    }
    mock_map_repository.load_map_data.return_value = map_data
    with pytest.raises(ValueError) as exc_info:
        place_manager.get_place(place_identifier)
    assert f"Place ID '{place_identifier}' not found." in str(exc_info)
    mock_map_repository.load_map_data.assert_called_once()


def test_get_place_template_success():
    place = {"id": "place1", "place_template": "template1"}
    result = PlaceManager.get_place_template(place)
    assert result == "template1"


def test_get_place_template_not_found():
    place = {"id": "place1"}
    with pytest.raises(ValueError) as exc_info:
        PlaceManager.get_place_template(place)
    assert "Place template not found for place ID 'place1'." in str(exc_info)


def test_determine_place_type_success(place_manager, mock_map_repository):
    place_identifier = "place1"
    place = {"id": "place1", "type": "area"}
    map_data = {"place1": place}
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.determine_place_type(place_identifier)
    assert result == TemplateType.AREA


def test_determine_place_type_invalid_type(place_manager, mock_map_repository):
    place_identifier = "place1"
    place = {"id": "place1", "type": "invalid_type"}
    map_data = {"place1": place}
    mock_map_repository.load_map_data.return_value = map_data
    with pytest.raises(ValueError) as exc_info:
        place_manager.determine_place_type(place_identifier)
    assert (
        f"Unknown place type 'invalid_type' for place ID '{place_identifier}'."
        in str(exc_info)
    )


def test_get_place_categories_success(place_manager, mock_template_repository):
    place_template = "template1"
    place_type = TemplateType.AREA
    templates = {
        "template1": {"categories": ["cat1", "cat2"]},
        "template2": {"categories": ["cat3"]},
    }
    mock_template_repository.load_template.return_value = templates
    result = place_manager.get_place_categories(place_template, place_type)
    expected_categories = ["cat1", "cat2"]
    assert result == expected_categories
    mock_template_repository.load_template.assert_called_once_with(place_type)


def test_get_place_categories_template_not_found(
    place_manager, mock_template_repository
):
    place_template = "nonexistent_template"
    place_type = TemplateType.AREA
    templates = {
        "template1": {"categories": ["cat1", "cat2"]},
        "template2": {"categories": ["cat3"]},
    }
    mock_template_repository.load_template.return_value = templates
    with pytest.raises(ValueError) as exc_info:
        place_manager.get_place_categories(place_template, place_type)
    assert f"'{place_template}' not found in {place_type} templates." in str(exc_info)
    mock_template_repository.load_template.assert_called_once_with(place_type)


def test_get_places_of_type_with_results(place_manager, mock_map_repository):
    place_type = TemplateType.AREA
    map_data = {
        "place1": {"type": "area", "place_template": "template1"},
        "place2": {"type": "location", "place_template": "template2"},
        "place3": {"type": "area", "place_template": "template3"},
    }
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.get_places_of_type(place_type)
    expected = ["template1", "template3"]
    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


def test_get_places_of_type_no_results(place_manager, mock_map_repository):
    place_type = TemplateType.REGION
    map_data = {
        "place1": {"type": "area", "place_template": "template1"},
        "place2": {"type": "location", "place_template": "template2"},
    }
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.get_places_of_type(place_type)
    expected = []
    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


def test_is_visited_true(place_manager, mock_map_repository):
    place_identifier = "place1"
    map_data = {"place1": {"visited": True}, "place2": {"visited": False}}
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.is_visited(place_identifier)
    assert result is True
    mock_map_repository.load_map_data.assert_called_once()


def test_is_visited_false(place_manager, mock_map_repository):
    place_identifier = "place2"
    map_data = {"place1": {"visited": True}, "place2": {"visited": False}}
    mock_map_repository.load_map_data.return_value = map_data
    result = place_manager.is_visited(place_identifier)
    assert result is False
    mock_map_repository.load_map_data.assert_called_once()


def test_set_as_visited_success(place_manager, mock_map_repository):
    place_identifier = "place1"
    map_data = {"place1": {"visited": False}, "place2": {"visited": False}}
    expected_map_data = {"place1": {"visited": True}, "place2": {"visited": False}}
    mock_map_repository.load_map_data.return_value = map_data
    place_manager.set_as_visited(place_identifier)
    assert map_data == expected_map_data
    mock_map_repository.save_map_data.assert_called_once_with(map_data)


def test_remove_character_from_place_success(place_manager, mock_map_repository):
    place_identifier = "place1"
    character_identifier_to_remove = "char1"
    place = {"id": "place1", "characters": ["char1", "char2", "char3"]}
    map_data = {"place1": place}
    mock_map_repository.load_map_data.return_value = map_data
    place_manager.get_place = Mock(return_value=place)
    place_manager.remove_character_from_place(
        character_identifier_to_remove, place_identifier
    )
    expected_characters = ["char2", "char3"]
    assert place["characters"] == expected_characters
    updated_map_data = {"place1": {"id": "place1", "characters": ["char2", "char3"]}}
    mock_map_repository.save_map_data.assert_called_once_with(updated_map_data)


def test_get_current_place_type_success(
    place_manager, mock_map_repository, mock_playthrough_manager
):
    current_place_id = "place1"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_id
    )
    place = {"id": current_place_id, "type": "area"}
    map_data = {current_place_id: place}
    mock_map_repository.load_map_data.return_value = map_data
    place_manager.get_place = Mock(return_value=place)
    result = place_manager.get_current_place_type()
    assert result == TemplateType.AREA


def test_add_location_success(
    place_manager, mock_map_repository, mock_playthrough_manager
):
    current_place_id = "area1"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_id
    )
    place_identifier = "location1"
    current_place = {"id": current_place_id, "type": "area", "locations": []}
    map_data = {current_place_id: current_place}
    mock_map_repository.load_map_data.return_value = map_data
    place_manager.get_current_place_type = Mock(return_value=TemplateType.AREA)
    place_manager.add_location(place_identifier)
    assert current_place["locations"] == ["location1"]
    mock_map_repository.save_map_data.assert_called_once_with(map_data)


def test_set_current_weather_success(
    place_manager, mock_map_repository, mock_playthrough_manager
):
    current_place_id = "area1"
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_id
    )
    weather_identifier = "weather1"
    current_place = {"id": current_place_id, "type": "area"}
    map_data = {current_place_id: current_place}
    mock_map_repository.load_map_data.return_value = map_data
    place_manager.get_current_place_type = Mock(return_value=TemplateType.AREA)
    place_manager.set_current_weather(weather_identifier)
    assert current_place["weather_identifier"] == "weather1"
    mock_map_repository.save_map_data.assert_called_once_with(map_data)
