# test_hierarchy_manager.py
from typing import cast
from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.base.required_string import RequiredString
from src.maps.hierarchy_manager import HierarchyManager
from src.maps.place_manager import PlaceManager


# Import the classes from your code
# Assuming they are available in the current scope
# If they are in a module, adjust the import statements accordingly
# from your_module import HierarchyManager, PlaceManager, RequiredString, TemplateType, PlacesTemplatesParameter


# Mock implementations of dependencies
class MockPlaceManager:
    def __init__(self, places_data, templates_data, place_types):
        self.places_data = places_data
        self.templates_data = templates_data
        self.place_types = place_types

    def get_place(self, place_identifier: RequiredString):
        return self.places_data.get(place_identifier.value)

    def determine_place_type(self, place_identifier: RequiredString):
        return self.place_types.get(place_identifier.value)

    def get_place_template(self, place):
        return self.templates_data.get(place["id"])


def test_get_place_hierarchy_location():
    # Create place identifiers
    world_id = RequiredString("world_1")
    region_id = RequiredString("region_1")
    area_id = RequiredString("area_1")
    location_id = RequiredString("location_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}
    region_place = {"id": region_id.value, "name": "Region 1", "world": world_id.value}
    area_place = {"id": area_id.value, "name": "Area 1", "region": region_id.value}
    location_place = {
        "id": location_id.value,
        "name": "Location 1",
        "area": area_id.value,
    }

    # Mock data
    places_data = {
        world_id.value: world_place,
        region_id.value: region_place,
        area_id.value: area_place,
        location_id.value: location_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
        region_id.value: TemplateType.REGION,
        area_id.value: TemplateType.AREA,
        location_id.value: TemplateType.LOCATION,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy
    hierarchy = hierarchy_manager.get_place_hierarchy(location_id)

    # Assertions
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] == area_place
    assert hierarchy["location"] == location_place


def test_get_place_hierarchy_area():
    # Create place identifiers
    world_id = RequiredString("world_1")
    region_id = RequiredString("region_1")
    area_id = RequiredString("area_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}
    region_place = {"id": region_id.value, "name": "Region 1", "world": world_id.value}
    area_place = {"id": area_id.value, "name": "Area 1", "region": region_id.value}

    # Mock data
    places_data = {
        world_id.value: world_place,
        region_id.value: region_place,
        area_id.value: area_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
        region_id.value: TemplateType.REGION,
        area_id.value: TemplateType.AREA,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy
    hierarchy = hierarchy_manager.get_place_hierarchy(area_id)

    # Assertions
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] == area_place
    assert hierarchy["location"] is None


def test_get_place_hierarchy_region():
    # Create place identifiers
    world_id = RequiredString("world_1")
    region_id = RequiredString("region_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}
    region_place = {"id": region_id.value, "name": "Region 1", "world": world_id.value}

    # Mock data
    places_data = {
        world_id.value: world_place,
        region_id.value: region_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
        region_id.value: TemplateType.REGION,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy
    hierarchy = hierarchy_manager.get_place_hierarchy(region_id)

    # Assertions
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] == region_place
    assert hierarchy["area"] is None
    assert hierarchy["location"] is None


def test_get_place_hierarchy_world():
    # Create place identifiers
    world_id = RequiredString("world_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}

    # Mock data
    places_data = {
        world_id.value: world_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy
    hierarchy = hierarchy_manager.get_place_hierarchy(world_id)

    # Assertions
    assert hierarchy["world"] == world_place
    assert hierarchy["region"] is None
    assert hierarchy["area"] is None
    assert hierarchy["location"] is None


def test_get_place_hierarchy_missing_world():
    # Create place identifiers
    area_id = RequiredString("area_1")

    # Create place data with missing 'region' and 'world'
    area_place = {"id": area_id.value, "name": "Area 1", "region": None}

    # Mock data
    places_data = {
        area_id.value: area_place,
    }
    place_types = {
        area_id.value: TemplateType.AREA,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy and expect an error
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.get_place_hierarchy(area_id)

    assert str(exc_info.value) == "Area didn't have a proper 'region' assigned."


def test_get_place_hierarchy_unhandled_place_type():
    # Create place identifiers
    place_id = RequiredString("unknown_place")

    # Create place data
    place = {"id": place_id.value, "name": "Unknown Place"}

    # Mock data
    places_data = {
        place_id.value: place,
    }
    place_types = {
        place_id.value: TemplateType.STORY_UNIVERSE,  # Unhandled type
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_place_hierarchy and expect an error
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.get_place_hierarchy(place_id)

    assert "Unhandled place type 'story_universe'." == str(exc_info.value)


def test_get_father_identifier_location():
    # Create place identifiers
    area_id = RequiredString("area_1")
    location_id = RequiredString("location_1")

    # Create place data
    location_place = {
        "id": location_id.value,
        "name": "Location 1",
        "area": area_id.value,
    }

    # Mock data
    places_data = {
        location_id.value: location_place,
    }
    place_types = {
        location_id.value: TemplateType.LOCATION,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_father_identifier
    father_identifier = hierarchy_manager.get_father_identifier(location_id)

    # Assertions
    assert father_identifier == area_id


def test_get_father_identifier_area():
    # Create place identifiers
    region_id = RequiredString("region_1")
    area_id = RequiredString("area_1")

    # Create place data
    area_place = {"id": area_id.value, "name": "Area 1", "region": region_id.value}

    # Mock data
    places_data = {
        area_id.value: area_place,
    }
    place_types = {
        area_id.value: TemplateType.AREA,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_father_identifier
    father_identifier = hierarchy_manager.get_father_identifier(area_id)

    # Assertions
    assert father_identifier == region_id


def test_get_father_identifier_region():
    # Create place identifiers
    world_id = RequiredString("world_1")
    region_id = RequiredString("region_1")

    # Create place data
    region_place = {"id": region_id.value, "name": "Region 1", "world": world_id.value}

    # Mock data
    places_data = {
        region_id.value: region_place,
    }
    place_types = {
        region_id.value: TemplateType.REGION,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_father_identifier
    father_identifier = hierarchy_manager.get_father_identifier(region_id)

    # Assertions
    assert father_identifier == world_id


def test_get_father_identifier_world():
    # Create place identifiers
    world_id = RequiredString("world_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}

    # Mock data
    places_data = {
        world_id.value: world_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call get_father_identifier and expect an error
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.get_father_identifier(world_id)

    assert f"Region '{world_id}' has no father identifier." == str(exc_info.value)


def test_fill_places_templates_parameter_location():
    # Create place identifiers
    world_id = RequiredString("world_1")
    region_id = RequiredString("region_1")
    area_id = RequiredString("area_1")
    location_id = RequiredString("location_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}
    region_place = {"id": region_id.value, "name": "Region 1", "world": world_id.value}
    area_place = {"id": area_id.value, "name": "Area 1", "region": region_id.value}
    location_place = {
        "id": location_id.value,
        "name": "Location 1",
        "area": area_id.value,
    }

    # Create templates
    templates_data = {
        world_id.value: RequiredString("world_template"),
        region_id.value: RequiredString("region_template"),
        area_id.value: RequiredString("area_template"),
        location_id.value: RequiredString("location_template"),
    }

    # Mock data
    places_data = {
        world_id.value: world_place,
        region_id.value: region_place,
        area_id.value: area_place,
        location_id.value: location_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
        region_id.value: TemplateType.REGION,
        area_id.value: TemplateType.AREA,
        location_id.value: TemplateType.LOCATION,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, templates_data, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call fill_places_templates_parameter
    places_templates_parameter = hierarchy_manager.fill_places_templates_parameter(
        location_id
    )

    # Assertions
    assert (
        places_templates_parameter.get_world_template()
        == templates_data[world_id.value]
    )
    assert (
        places_templates_parameter.get_region_template()
        == templates_data[region_id.value]
    )
    assert (
        places_templates_parameter.get_area_template() == templates_data[area_id.value]
    )
    assert (
        places_templates_parameter.get_location_template()
        == templates_data[location_id.value]
    )


def test_fill_places_templates_parameter_area_no_region():
    # Create place identifiers
    world_id = RequiredString("world_1")
    area_id = RequiredString("area_1")

    # Create place data
    world_place = {"id": world_id.value, "name": "World 1"}
    area_place = {"id": area_id.value, "name": "Area 1", "world": world_id.value}

    # Create templates
    templates_data = {
        world_id.value: RequiredString("world_template"),
        area_id.value: RequiredString("area_template"),
    }

    # Mock data
    places_data = {
        world_id.value: world_place,
        area_id.value: area_place,
    }
    place_types = {
        world_id.value: TemplateType.WORLD,
        area_id.value: TemplateType.AREA,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, templates_data, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call fill_places_templates_parameter
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.fill_places_templates_parameter(area_id)

    # Assertions
    assert "Area didn't have 'region' assigned." == str(exc_info.value)


def test_fill_places_templates_parameter_missing_world():
    # Create place identifiers
    area_id = RequiredString("area_1")

    # Create place data with missing 'world'
    area_place = {"id": area_id.value, "name": "Area 1", "region": None}

    # Mock data
    places_data = {
        area_id.value: area_place,
    }
    place_types = {
        area_id.value: TemplateType.AREA,
    }

    # Create a mock PlaceManager
    place_manager = MockPlaceManager(places_data, {}, place_types)

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(cast(PlaceManager, place_manager))

    # Call fill_places_templates_parameter and expect an error
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.fill_places_templates_parameter(area_id)

    assert str(exc_info.value) == "Area didn't have a proper 'region' assigned."


def test_fill_places_templates_parameter_empty_identifier():
    # Create a mock PlaceManager
    place_manager = Mock()

    # Create HierarchyManager instance
    hierarchy_manager = HierarchyManager(place_manager)

    # Call fill_places_templates_parameter with empty identifier and expect an error
    with pytest.raises(ValueError) as exc_info:
        hierarchy_manager.fill_places_templates_parameter(RequiredString(""))

    assert str(exc_info.value) == "value can't be empty."
