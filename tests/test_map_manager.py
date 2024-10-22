from enum import Enum
from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.maps.map_manager import MapManager


def test_map_manager_init_with_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        MapManager(
            playthrough_name="",
            place_manager=Mock(),
            hierarchy_manager=Mock(),
            map_repository=Mock(),
            template_repository=Mock(),
            identifiers_manager=Mock(),
            playthrough_manager=Mock(),
        )
    assert "must be a non-empty" in str(exc_info)


def test_map_manager_init_with_valid_playthrough_name():
    playthrough_name = "playthrough1"
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    map_manager = MapManager(
        playthrough_name=playthrough_name,
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    assert map_manager._place_manager == place_manager
    assert map_manager._hierarchy_manager == hierarchy_manager
    assert map_manager._map_repository == map_repository
    assert map_manager._template_repository == template_repository
    assert map_manager._identifiers_manager == identifiers_manager
    assert map_manager._playthrough_manager == playthrough_manager


def test_map_manager_init_without_optional_managers():
    playthrough_name = "playthrough1"
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    map_manager = MapManager(
        playthrough_name=playthrough_name,
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
    )
    assert map_manager._identifiers_manager is not None
    assert map_manager._playthrough_manager is not None


def test_get_current_place_template():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_1"
    place_manager.get_place.return_value = "place_data"
    place_manager.get_place_template.return_value = "template_1"
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_current_place_template()
    assert result == "template_1"
    playthrough_manager.get_current_place_identifier.assert_called_once()
    place_manager.get_place.assert_called_once_with("place_id_1")
    place_manager.get_place_template.assert_called_once_with("place_data")


def test_get_current_area_when_current_place_is_area():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_area"
    place_manager.get_current_place_type.return_value = TemplateType.AREA
    fake_map_data = {"place_id_area": {"info": "area_data"}}
    map_repository.load_map_data.return_value = fake_map_data
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_current_area()
    assert result == {"info": "area_data"}
    map_repository.load_map_data.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    playthrough_manager.get_current_place_identifier.assert_called_once()


def test_get_current_area_when_current_place_is_location():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_location"
    place_manager.get_current_place_type.side_effect = [
        TemplateType.LOCATION,
        TemplateType.LOCATION,
    ]
    fake_map_data = {
        "place_id_location": {"area": "area_1"},
        "area_1": {"info": "area_data"},
    }
    map_repository.load_map_data.return_value = fake_map_data
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_current_area()
    assert result == {"info": "area_data"}
    map_repository.load_map_data.assert_called_once()
    assert place_manager.get_current_place_type.call_count == 2
    playthrough_manager.get_current_place_identifier.assert_called_once()


def test_get_father_template_when_current_place_is_location():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_location"
    places_parameter_mock = Mock()
    places_parameter_mock.get_area_template.return_value = "area_template"
    hierarchy_manager.fill_places_templates_parameter.return_value = (
        places_parameter_mock
    )
    place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_father_template()
    assert result == "area_template"
    playthrough_manager.get_current_place_identifier.assert_called_once()
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        "place_id_location"
    )
    place_manager.get_current_place_type.assert_called_once()
    places_parameter_mock.get_area_template.assert_called_once()


def test_get_father_template_when_current_place_is_area():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_area"
    places_parameter_mock = Mock()
    places_parameter_mock.get_region_template.return_value = "region_template"
    hierarchy_manager.fill_places_templates_parameter.return_value = (
        places_parameter_mock
    )
    place_manager.get_current_place_type.return_value = TemplateType.AREA
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_father_template()
    assert result == "region_template"
    playthrough_manager.get_current_place_identifier.assert_called_once()
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        "place_id_area"
    )
    place_manager.get_current_place_type.assert_called_once()
    places_parameter_mock.get_region_template.assert_called_once()


def test_get_father_template_when_current_place_is_region():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    playthrough_manager.get_current_place_identifier.return_value = "place_id_region"
    places_parameter_mock = Mock()
    places_parameter_mock.get_world_template.return_value = "world_template"
    hierarchy_manager.fill_places_templates_parameter.return_value = (
        places_parameter_mock
    )
    place_manager.get_current_place_type.return_value = TemplateType.REGION
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_father_template()
    assert result == "world_template"
    playthrough_manager.get_current_place_identifier.assert_called_once()
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        "place_id_region"
    )
    place_manager.get_current_place_type.assert_called_once()
    places_parameter_mock.get_world_template.assert_called_once()


def test_get_father_template_when_current_place_type_is_unhandled():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()

    class FakeTemplateType(Enum):
        UNHANDLED = "unhandled"

    place_manager.get_current_place_type.return_value = FakeTemplateType.UNHANDLED
    playthrough_manager.get_current_place_identifier.return_value = "place_id_unhandled"
    hierarchy_manager.fill_places_templates_parameter.return_value = Mock()
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    with pytest.raises(ValueError) as exc_info:
        map_manager.get_father_template()
    assert "This function isn't prepared to handle the place type" in str(exc_info)
    playthrough_manager.get_current_place_identifier.assert_called_once()
    place_manager.get_current_place_type.assert_called_once()
    hierarchy_manager.fill_places_templates_parameter.assert_called_once()


def test_get_identifier_and_place_template_of_latest_map_entry():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    fake_map_data = {"id1": {}, "id2": {}, "id3": {}}
    map_repository.load_map_data.return_value = fake_map_data
    identifiers_manager.get_highest_identifier.return_value = "id3"
    place_manager.get_place.return_value = "place_data_latest"
    place_manager.get_place_template.return_value = "latest_template"
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result_id, result_template = (
        map_manager.get_identifier_and_place_template_of_latest_map_entry()
    )
    assert result_id == "id3"
    assert result_template == "latest_template"
    map_repository.load_map_data.assert_called_once()
    identifiers_manager.get_highest_identifier.assert_called_once_with(fake_map_data)
    place_manager.get_place.assert_called_once_with("id3")
    place_manager.get_place_template.assert_called_once_with("place_data_latest")


def test_get_place_full_data_with_all_place_types():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    place_identifier = "location1"
    hierarchy_manager.get_place_hierarchy.return_value = {
        "location": "location_place",
        "area": "area_place",
        "region": "region_place",
        "world": "world_place",
    }
    place_manager.get_place_template.side_effect = [
        "world_template",
        "region_template",
        "area_template",
        "location_template",
    ]

    def load_template_side_effect(template_type):
        templates_dict = {
            TemplateType.LOCATION: {
                "location_template": {"description": "Location description"}
            },
            TemplateType.AREA: {"area_template": {"description": "Area description"}},
            TemplateType.REGION: {
                "region_template": {"description": "Region description"}
            },
            TemplateType.WORLD: {
                "world_template": {"description": "World description"}
            },
        }
        return templates_dict.get(template_type, {})

    template_repository.load_template.side_effect = load_template_side_effect
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_place_full_data(place_identifier)
    expected_result = {
        "world_data": {"name": "world_template", "description": "World description"},
        "region_data": {"name": "region_template", "description": "Region description"},
        "area_data": {"name": "area_template", "description": "Area description"},
        "location_data": {
            "name": "location_template",
            "description": "Location description",
        },
    }
    assert result == expected_result
    hierarchy_manager.get_place_hierarchy.assert_called_once_with(place_identifier)
    assert place_manager.get_place_template.call_count == 4
    assert template_repository.load_template.call_count == 4


def test_get_place_full_data_with_missing_place_types():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    place_identifier = "location1"
    hierarchy_manager.get_place_hierarchy.return_value = {
        "location": "location_place",
        "area": None,
        "region": "region_place",
        "world": None,
    }
    place_manager.get_place_template.side_effect = [
        "region_template",
        "location_template",
    ]

    def load_template_side_effect(template_type):
        templates_dict = {
            TemplateType.LOCATION: {
                "location_template": {"description": "Location description"}
            },
            TemplateType.REGION: {
                "region_template": {"description": "Region description"}
            },
        }
        return templates_dict.get(template_type, {})

    template_repository.load_template.side_effect = load_template_side_effect
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_place_full_data(place_identifier)
    expected_result = {
        "world_data": None,
        "region_data": {"name": "region_template", "description": "Region description"},
        "area_data": None,
        "location_data": {
            "name": "location_template",
            "description": "Location description",
        },
    }
    assert result == expected_result
    hierarchy_manager.get_place_hierarchy.assert_called_once_with(place_identifier)
    assert place_manager.get_place_template.call_count == 2
    assert template_repository.load_template.call_count == 2


def test_get_place_full_data_with_missing_template_data():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    place_identifier = "location1"
    hierarchy_manager.get_place_hierarchy.return_value = {
        "location": "location_place",
        "area": None,
        "region": None,
        "world": None,
    }
    place_manager.get_place_template.return_value = "location_template"
    template_repository.load_template.return_value = {}
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    with pytest.raises(ValueError) as exc_info:
        map_manager.get_place_full_data(place_identifier)
    assert "Location template 'location_template' not found." in str(exc_info)
    hierarchy_manager.get_place_hierarchy.assert_called_once_with(place_identifier)
    place_manager.get_place_template.assert_called_once_with("location_place")
    template_repository.load_template.assert_called_once_with(TemplateType("location"))


def test_get_locations_in_area_with_locations():
    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    area_identifier = "area1"
    fake_map_data = {
        "location1": {
            "area": "area1",
            "type": "location",
            "place_template": "template1",
        },
        "location2": {
            "area": "area1",
            "type": "location",
            "place_template": "template2",
        },
        "location3": {
            "area": "area2",
            "type": "location",
            "place_template": "template3",
        },
        "area1": {"type": "area"},
    }
    map_repository.load_map_data.return_value = fake_map_data
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    result = map_manager.get_locations_in_area(area_identifier)
    expected_result = [
        {"identifier": "location1", "place_template": "template1"},
        {"identifier": "location2", "place_template": "template2"},
    ]
    assert result == expected_result
    map_repository.load_map_data.assert_called_once()


def test_get_locations_in_area_no_locations(caplog):
    import logging

    place_manager = Mock()
    hierarchy_manager = Mock()
    map_repository = Mock()
    template_repository = Mock()
    identifiers_manager = Mock()
    playthrough_manager = Mock()
    area_identifier = "area_no_locations"
    fake_map_data = {
        "location1": {
            "area": "area1",
            "type": "location",
            "place_template": "template1",
        },
        "area1": {"type": "area"},
        "area_no_locations": {"type": "area"},
    }
    map_repository.load_map_data.return_value = fake_map_data
    map_manager = MapManager(
        playthrough_name="playthrough1",
        place_manager=place_manager,
        hierarchy_manager=hierarchy_manager,
        map_repository=map_repository,
        template_repository=template_repository,
        identifiers_manager=identifiers_manager,
        playthrough_manager=playthrough_manager,
    )
    with caplog.at_level(logging.WARNING):
        result = map_manager.get_locations_in_area(area_identifier)
    assert result == []
    map_repository.load_map_data.assert_called_once()
    assert f"No locations found in area '{area_identifier}'." in caplog.text
