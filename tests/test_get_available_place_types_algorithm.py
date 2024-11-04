from unittest.mock import Mock, patch

import pytest

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_selection_manager import PlaceSelectionManager
from src.maps.templates_repository import TemplatesRepository


def test_init_with_valid_parameters():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )

    assert algorithm._playthrough_name == playthrough_name
    assert algorithm._current_place_template == current_place_template
    assert algorithm._place_type == place_type
    assert algorithm._place_manager_factory == place_manager_factory
    assert algorithm._place_selection_manager == place_selection_manager
    assert algorithm._templates_repository == templates_repository


def test_init_with_empty_playthrough_name_should_raise_error():
    playthrough_name = ""
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)

    with pytest.raises(ValueError):
        GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place_template,
            place_type,
            place_manager_factory,
            place_selection_manager,
        )


def test_init_with_empty_current_place_template_should_raise_error():
    playthrough_name = "test_playthrough"
    current_place_template = ""
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)

    with pytest.raises(ValueError):
        GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place_template,
            place_type,
            place_manager_factory,
            place_selection_manager,
        )


def test_init_with_invalid_place_type_should_raise_type_error():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.WORLD  # Invalid place_type
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)

    with pytest.raises(TypeError):
        GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place_template,
            place_type,
            place_manager_factory,
            place_selection_manager,
        )


def test_do_algorithm_returns_correct_list_when_available_places_exist():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"type": "type1"},
        "template2": {"type": "type2"},
        "template3": {"type": "type3"},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    place_categories = ["category1", "category2"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = {
        "template1": {"type": "type1"},
        "template2": {"type": "type2"},
    }
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = ["template2"]
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = ["type1"]

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert set(result) == set(expected_types)


def test_do_algorithm_returns_empty_list_when_no_available_places():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"type": "type1"},
        "template2": {"type": "type2"},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = {}
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = []
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = []

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert result == expected_types


def test_do_algorithm_returns_empty_list_when_all_places_are_used():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"type": "type1"},
        "template2": {"type": "type2"},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = location_templates
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = ["template1", "template2"]
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = []

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert result == expected_types


def test_do_algorithm_with_empty_templates_repository():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {}
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = {}
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = []
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = []

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert result == expected_types


def test_do_algorithm_ignores_places_without_type_field():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"name": "Place One"},
        "template2": {"type": "type2"},
        "template3": {"type": None},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = location_templates
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = []
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = ["type2"]

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert result == expected_types


def test_do_algorithm_ignores_places_with_none_or_empty_type():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"type": ""},
        "template2": {"type": None},
        "template3": {"type": "type3"},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = location_templates
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = []
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = ["type3"]

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert result == expected_types


def test_do_algorithm_returns_unique_types():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)
    templates_repository = Mock(spec=TemplatesRepository)

    location_templates = {
        "template1": {"type": "type1"},
        "template2": {"type": "type1"},
        "template3": {"type": "type2"},
    }
    templates_repository.load_templates.return_value = location_templates

    place_manager = Mock()
    place_manager_factory.create_place_manager.return_value = place_manager

    parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
    place_categories = ["category1"]
    place_manager.get_place_categories.return_value = place_categories

    filtered_places = location_templates
    place_selection_manager.filter_places_by_categories.return_value = filtered_places

    used_templates = []
    place_manager.get_places_of_type.return_value = used_templates

    expected_types = ["type1", "type2"]

    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name,
        current_place_template,
        place_type,
        place_manager_factory,
        place_selection_manager,
        templates_repository,
    )
    result = algorithm.do_algorithm()

    assert set(result) == set(expected_types)


def test_do_algorithm_with_default_templates_repository():
    playthrough_name = "test_playthrough"
    current_place_template = "test_place_template"
    place_type = TemplateType.LOCATION
    place_manager_factory = Mock(spec=PlaceManagerFactory)
    place_selection_manager = Mock(spec=PlaceSelectionManager)

    with patch(
        "src.maps.algorithms.get_available_place_types_algorithm.TemplatesRepository"
    ) as MockTemplatesRepository:
        templates_repository_instance = Mock()
        MockTemplatesRepository.return_value = templates_repository_instance

        location_templates = {
            "template1": {"type": "type1"},
            "template2": {"type": "type2"},
        }
        templates_repository_instance.load_templates.return_value = location_templates

        place_manager = Mock()
        place_manager_factory.create_place_manager.return_value = place_manager

        parent_template_type = PARENT_TEMPLATE_TYPE.get(place_type)
        place_categories = ["category1"]
        place_manager.get_place_categories.return_value = place_categories

        filtered_places = location_templates
        place_selection_manager.filter_places_by_categories.return_value = (
            filtered_places
        )

        used_templates = []
        place_manager.get_places_of_type.return_value = used_templates

        expected_types = ["type1", "type2"]

        algorithm = GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place_template,
            place_type,
            place_manager_factory,
            place_selection_manager,
        )
        result = algorithm.do_algorithm()

        assert set(result) == set(expected_types)
        MockTemplatesRepository.assert_called_once()
