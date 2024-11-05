# test_get_place_full_data_algorithm.py

from unittest.mock import Mock

import pytest

from src.base.enums import TemplateType
from src.maps.algorithms.get_place_full_data_algorithm import GetPlaceFullDataAlgorithm


# Assuming the GetPlaceFullDataAlgorithm and related Enums are imported from the module
# from your_module import GetPlaceFullDataAlgorithm, TemplateType


# Test when all places are present and templates are available
def test_do_algorithm_all_places_present():
    place_identifier = "test_place"

    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()
    templates_repository = Mock()

    hierarchy_manager = Mock()
    hierarchy_manager.get_place_hierarchy.return_value = {
        "world": "world_place",
        "region": "region_place",
        "area": "area_place",
        "location": "location_place",
        "room": "room_place",
    }
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager

    place_manager = Mock()
    place_manager.get_place_template.side_effect = lambda place: f"{place}_template"
    place_manager_factory.create_place_manager.return_value = place_manager

    templates_repository.load_templates.side_effect = lambda template_type: {
        f"{template_type.value}_place_template": {
            "description": f"{template_type.value} description"
        }
    }

    algorithm = GetPlaceFullDataAlgorithm(
        place_identifier,
        place_manager_factory,
        hierarchy_manager_factory,
        templates_repository,
    )

    result = algorithm.do_algorithm()

    expected_result = {
        "world_data": {
            "name": "world_place_template",
            "description": "world description",
        },
        "region_data": {
            "name": "region_place_template",
            "description": "region description",
        },
        "area_data": {"name": "area_place_template", "description": "area description"},
        "location_data": {
            "name": "location_place_template",
            "description": "location description",
        },
        "room_data": {"name": "room_place_template", "description": "room description"},
    }

    assert result == expected_result


# Test when some places are missing in the hierarchy
def test_do_algorithm_some_places_missing():
    place_identifier = "test_place"

    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()
    templates_repository = Mock()

    hierarchy_manager = Mock()
    hierarchy_manager.get_place_hierarchy.return_value = {
        "world": "world_place",
        "area": "area_place",
        "room": "room_place",
    }
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager

    place_manager = Mock()
    place_manager.get_place_template.side_effect = lambda place: f"{place}_template"
    place_manager_factory.create_place_manager.return_value = place_manager

    templates_repository.load_templates.side_effect = lambda template_type: {
        f"{template_type.value}_place_template": {
            "description": f"{template_type.value} description"
        }
    }

    algorithm = GetPlaceFullDataAlgorithm(
        place_identifier,
        place_manager_factory,
        hierarchy_manager_factory,
        templates_repository,
    )

    result = algorithm.do_algorithm()

    expected_result = {
        "world_data": {
            "name": "world_place_template",
            "description": "world description",
        },
        "region_data": None,
        "area_data": {"name": "area_place_template", "description": "area description"},
        "location_data": None,
        "room_data": {"name": "room_place_template", "description": "room description"},
    }

    assert result == expected_result


# Test when template data is missing, expecting a ValueError
def test_do_algorithm_template_data_missing():
    place_identifier = "test_place"

    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()
    templates_repository = Mock()

    hierarchy_manager = Mock()
    hierarchy_manager.get_place_hierarchy.return_value = {
        "world": "world_place",
        "region": "region_place",
        "area": "area_place",
        "location": "location_place",
        "room": "room_place",
    }
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager

    place_manager = Mock()
    place_manager.get_place_template.side_effect = lambda place: f"{place}_template"
    place_manager_factory.create_place_manager.return_value = place_manager

    def load_templates(template_type):
        if template_type == TemplateType.ROOM:
            return {}
        else:
            return {
                f"{template_type.value}_place_template": {
                    "description": f"{template_type.value} description"
                }
            }

    templates_repository.load_templates.side_effect = load_templates

    algorithm = GetPlaceFullDataAlgorithm(
        place_identifier,
        place_manager_factory,
        hierarchy_manager_factory,
        templates_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algorithm.do_algorithm()

    assert (
        "Template name 'room_place_template' not present in the templates for 'room'"
        in str(exc_info.value)
    )


# Test initialization with an empty place_identifier, expecting a ValueError
def test_init_with_empty_place_identifier():
    place_identifier = ""
    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()

    with pytest.raises(ValueError) as exc_info:
        GetPlaceFullDataAlgorithm(
            place_identifier, place_manager_factory, hierarchy_manager_factory
        )

    assert "'place_identifier' must be" in str(exc_info.value)


# Test initialization without templates_repository, expecting default initialization
def test_init_without_templates_repository():
    place_identifier = "test_place"
    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()

    algorithm = GetPlaceFullDataAlgorithm(
        place_identifier, place_manager_factory, hierarchy_manager_factory
    )

    assert algorithm._templates_repository is not None


# Test when template data is missing the 'description' key
def test_do_algorithm_template_data_missing_description():
    place_identifier = "test_place"

    place_manager_factory = Mock()
    hierarchy_manager_factory = Mock()
    templates_repository = Mock()

    hierarchy_manager = Mock()
    hierarchy_manager.get_place_hierarchy.return_value = {"world": "world_place"}
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager

    place_manager = Mock()
    place_manager.get_place_template.return_value = "world_place_template"
    place_manager_factory.create_place_manager.return_value = place_manager

    templates_repository.load_templates.return_value = {"world_place_template": {}}

    algorithm = GetPlaceFullDataAlgorithm(
        place_identifier,
        place_manager_factory,
        hierarchy_manager_factory,
        templates_repository,
    )

    with pytest.raises(ValueError) as exc_info:
        result = algorithm.do_algorithm()

    assert "World template data is missing" in str(exc_info.value)
