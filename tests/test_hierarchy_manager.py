from typing import cast

import pytest

from src.base.enums import TemplateType
from src.maps.hierarchy_manager import HierarchyManager
from src.maps.place_manager import PlaceManager


class MockPlaceManager:

    def __init__(self, places_data, templates_data, place_types):
        self.places_data = places_data
        self.templates_data = templates_data
        self.place_types = place_types

    def get_place(self, place_identifier: str):
        return self.places_data.get(place_identifier)

    def determine_place_type(self, place_identifier: str):
        return self.place_types.get(place_identifier)

    def get_place_template(self, place):
        return self.templates_data.get(place["id"])


def test_get_place_hierarchy_location():
    world_id = "world_1"
    region_id = "region_1"
    area_id = "area_1"
    location_id = "location_1"
    world_place = {"id": world_id, "name": "World 1"}
    region_place = {"id": region_id, "name": "Region 1", "world": world_id}
    area_place = {"id": area_id, "name": "Area 1", "region": region_id}
    location_place = {"id": location_id, "name": "Location 1", "area": area_id}
    places_data = {
        world_id: world_place,
        region_id: region_place,
        area_id: area_place,
        location_id: location_place,
    }
    place_types = {
        world_id: TemplateType.WORLD,
        region_id: TemplateType.REGION,
        area_id: TemplateType.AREA,
        location_id: TemplateType.LOCATION,
    }
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    hierarchy = hierarchy_manager.get_place_hierarchy(location_id)
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] == area_place
    assert hierarchy["location"] == location_place


def test_get_place_hierarchy_area():
    world_id = "world_1"
    region_id = "region_1"
    area_id = "area_1"
    world_place = {"id": world_id, "name": "World 1"}
    region_place = {"id": region_id, "name": "Region 1", "world": world_id}
    area_place = {"id": area_id, "name": "Area 1", "region": region_id}
    places_data = {world_id: world_place, region_id: region_place, area_id: area_place}
    place_types = {
        world_id: TemplateType.WORLD,
        region_id: TemplateType.REGION,
        area_id: TemplateType.AREA,
    }
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    hierarchy = hierarchy_manager.get_place_hierarchy(area_id)
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] == area_place
    assert hierarchy["location"] is None


def test_get_place_hierarchy_region():
    world_id = "world_1"
    region_id = "region_1"
    world_place = {"id": world_id, "name": "World 1"}
    region_place = {"id": region_id, "name": "Region 1", "world": world_id}
    places_data = {world_id: world_place, region_id: region_place}
    place_types = {world_id: TemplateType.WORLD, region_id: TemplateType.REGION}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    hierarchy = hierarchy_manager.get_place_hierarchy(region_id)
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] is None
    assert hierarchy["location"] is None


def test_get_place_hierarchy_world():
    world_id = "world_1"
    world_place = {"id": world_id, "name": "World 1"}
    places_data = {world_id: world_place}
    place_types = {world_id: TemplateType.WORLD}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    hierarchy = hierarchy_manager.get_place_hierarchy(world_id)
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] is None
    assert hierarchy["area"] is None
    assert hierarchy["location"] is None


def test_get_place_hierarchy_unhandled_place_type():
    place_id = "unknown_place"
    place = {"id": place_id, "name": "Unknown Place"}
    places_data = {place_id: place}
    place_types = {place_id: TemplateType.STORY_UNIVERSE}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.get_place_hierarchy(place_id)
    assert "Unhandled place type 'story_universe'." in str(exc_info)


def test_get_father_identifier_location():
    area_id = "area_1"
    location_id = "location_1"
    location_place = {"id": location_id, "name": "Location 1", "area": area_id}
    places_data = {location_id: location_place}
    place_types = {location_id: TemplateType.LOCATION}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    father_identifier = hierarchy_manager.get_father_identifier(location_id)
    assert father_identifier == area_id


def test_get_father_identifier_area():
    region_id = "region_1"
    area_id = "area_1"
    area_place = {"id": area_id, "name": "Area 1", "region": region_id}
    places_data = {area_id: area_place}
    place_types = {area_id: TemplateType.AREA}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    father_identifier = hierarchy_manager.get_father_identifier(area_id)
    assert father_identifier == region_id


def test_get_father_identifier_region():
    world_id = "world_1"
    region_id = "region_1"
    region_place = {"id": region_id, "name": "Region 1", "world": world_id}
    places_data = {region_id: region_place}
    place_types = {region_id: TemplateType.REGION}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    father_identifier = hierarchy_manager.get_father_identifier(region_id)
    assert father_identifier == world_id


def test_get_father_identifier_world():
    world_id = "world_1"
    world_place = {"id": world_id, "name": "World 1"}
    places_data = {world_id: world_place}
    place_types = {world_id: TemplateType.WORLD}
    place_manager = MockPlaceManager(places_data, {}, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.get_father_identifier(world_id)
    assert f"Region '{world_id}' has no father identifier." in str(exc_info)


def test_fill_places_templates_parameter_location():
    world_id = "world_1"
    region_id = "region_1"
    area_id = "area_1"
    location_id = "location_1"
    world_place = {"id": world_id, "name": "World 1"}
    region_place = {"id": region_id, "name": "Region 1", "world": world_id}
    area_place = {"id": area_id, "name": "Area 1", "region": region_id}
    location_place = {"id": location_id, "name": "Location 1", "area": area_id}
    templates_data = {
        world_id: "world_template",
        region_id: "region_template",
        area_id: "area_template",
        location_id: "location_template",
    }
    places_data = {
        world_id: world_place,
        region_id: region_place,
        area_id: area_place,
        location_id: location_place,
    }
    place_types = {
        world_id: TemplateType.WORLD,
        region_id: TemplateType.REGION,
        area_id: TemplateType.AREA,
        location_id: TemplateType.LOCATION,
    }
    place_manager = MockPlaceManager(places_data, templates_data, place_types)
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))
    places_templates_parameter = hierarchy_manager.fill_places_templates_parameter(
        location_id
    )
    assert places_templates_parameter.get_world_template() == templates_data[world_id]
    assert places_templates_parameter.get_region_template() == templates_data[region_id]
    assert places_templates_parameter.get_area_template() == templates_data[area_id]
    assert (
        places_templates_parameter.get_location_template()
        == templates_data[location_id]
    )
