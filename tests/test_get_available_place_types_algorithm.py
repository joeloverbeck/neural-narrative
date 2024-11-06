# test_get_available_place_types_algorithm.py
import logging
from unittest.mock import MagicMock, patch

import pytest

from src.base.enums import TemplateType
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


# Assuming GetAvailablePlaceTypesAlgorithm is located in src.maps.algorithms.get_available_place_types_algorithm


# Fixtures for dependencies
@pytest.fixture
def mock_filter_places_by_categories_algorithm_factory():
    return MagicMock(spec=FilterPlacesByCategoriesAlgorithmFactory)


@pytest.fixture
def mock_place_manager_factory():
    return MagicMock(spec=PlaceManagerFactory)


@pytest.fixture
def mock_templates_repository():
    return MagicMock(spec=TemplatesRepository)


@pytest.fixture
def valid_playthrough_name():
    return "valid_playthrough"


@pytest.fixture
def valid_father_place_template():
    return "valid_father_template"


@pytest.fixture
def valid_father_place_type():
    return TemplateType.ROOM


@pytest.fixture
def valid_place_type():
    return TemplateType.LOCATION


@pytest.fixture
def algorithm_instance(
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
    valid_playthrough_name,
    valid_father_place_template,
    valid_father_place_type,
    valid_place_type,
):
    return GetAvailablePlaceTypesAlgorithm(
        playthrough_name=valid_playthrough_name,
        father_place_template=valid_father_place_template,
        father_place_type=valid_father_place_type,
        place_type=valid_place_type,
        filter_places_by_categories_algorithm_factory=mock_filter_places_by_categories_algorithm_factory,
        place_manager_factory=mock_place_manager_factory,
        templates_repository=mock_templates_repository,
    )


# Initialization Tests
def test_initialization_with_empty_playthrough_name(
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
    valid_father_place_template,
    valid_father_place_type,
    valid_place_type,
):
    with pytest.raises(ValueError) as exc_info:
        GetAvailablePlaceTypesAlgorithm(
            playthrough_name="",
            father_place_template=valid_father_place_template,
            father_place_type=valid_father_place_type,
            place_type=valid_place_type,
            filter_places_by_categories_algorithm_factory=mock_filter_places_by_categories_algorithm_factory,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )
    assert "playthrough_name" in str(exc_info.value)


def test_initialization_with_empty_father_place_template(
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
    valid_playthrough_name,
    valid_father_place_type,
    valid_place_type,
):
    with pytest.raises(ValueError) as exc_info:
        GetAvailablePlaceTypesAlgorithm(
            playthrough_name=valid_playthrough_name,
            father_place_template="",
            father_place_type=valid_father_place_type,
            place_type=valid_place_type,
            filter_places_by_categories_algorithm_factory=mock_filter_places_by_categories_algorithm_factory,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )
    assert "father_place_template" in str(exc_info.value)


# do_algorithm Tests
def test_do_algorithm_returns_available_places(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock templates_repository.load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
        "place3": {"category": "cat3"},
    }

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1", "cat2"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
    }
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Mock get_places_of_type
    mock_place_manager.get_places_of_type.return_value = ["place3"]

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert "place1" in available_places
    assert "place2" in available_places
    mock_templates_repository.load_templates.assert_called_once_with(
        algorithm_instance._place_type
    )
    mock_place_manager.get_place_categories.assert_called_once_with(
        algorithm_instance._father_place_template, algorithm_instance._father_place_type
    )
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.assert_called_once_with(
        mock_templates_repository.load_templates.return_value,
        mock_place_manager.get_place_categories.return_value,
    )
    mock_filter_algorithm.do_algorithm.assert_called_once()
    mock_place_manager.get_places_of_type.assert_called_once_with(
        algorithm_instance._place_type
    )


def test_do_algorithm_returns_empty_when_filtered_places_empty(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
    caplog,
):
    caplog.set_level(logging.WARNING)

    # Mock templates_repository.load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
    }

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat3"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {}
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert available_places == []
    assert any("No filtered places for" in record.message for record in caplog.records)


def test_do_algorithm_excludes_used_templates(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock templates_repository.load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
        "place3": {"category": "cat3"},
        "place4": {"category": "cat4"},
    }

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = [
        "cat1",
        "cat2",
        "cat3",
        "cat4",
    ]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
        "place3": {"category": "cat3"},
        "place4": {"category": "cat4"},
    }
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Mock get_places_of_type with some used templates
    mock_place_manager.get_places_of_type.return_value = ["place2", "place4"]

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert set(available_places) == {"place1", "place3"}


def test_do_algorithm_with_no_templates(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock templates_repository.load_templates to return empty dict
    mock_templates_repository.load_templates.return_value = {}

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {}
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert available_places == []


def test_do_algorithm_handles_no_used_templates(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock templates_repository.load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
    }

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1", "cat2"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {
        "place1": {"category": "cat1"},
        "place2": {"category": "cat2"},
    }
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Mock get_places_of_type with no used templates
    mock_place_manager.get_places_of_type.return_value = []

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert set(available_places) == {"place1", "place2"}


def test_do_algorithm_with_duplicate_available_places(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock templates_repository.load_templates with duplicate identifiers
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},  # noqa
        "place2": {"category": "cat2"},
        "place1": {"category": "cat1"},  # Duplicate key # noqa
    }

    # Mock place_manager.get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1", "cat2"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter_places_by_categories_algorithm with duplicate identifiers
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {
        "place1": {"category": "cat1"},  # noqa
        "place2": {"category": "cat2"},
        "place1": {"category": "cat1"},  # Duplicate key # noqa
    }
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Mock get_places_of_type
    mock_place_manager.get_places_of_type.return_value = []

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    # Since dictionaries cannot have duplicate keys, duplicates are inherently handled.
    assert set(available_places) == {"place1", "place2"}


def test_do_algorithm_with_none_templates_repository():
    # Test that the algorithm uses a new TemplatesRepository if none is provided

    with patch(
        "src.maps.algorithms.get_available_place_types_algorithm.TemplatesRepository"
    ) as MockTemplatesRepo:
        mock_templates_repo_instance = MagicMock()
        MockTemplatesRepo.return_value = mock_templates_repo_instance

        # Create instance without providing templates_repository
        algorithm = GetAvailablePlaceTypesAlgorithm(
            playthrough_name="playthrough",
            father_place_template="father_template",
            father_place_type=TemplateType.ROOM,
            place_type=TemplateType.LOCATION,
            filter_places_by_categories_algorithm_factory=MagicMock(),
            place_manager_factory=MagicMock(),
            templates_repository=None,
        )

        # Execute do_algorithm (it will use the mocked templates repository)
        mock_templates_repo_instance.load_templates.return_value = {}
        algorithm.do_algorithm()

        # Ensure TemplatesRepository was instantiated
        MockTemplatesRepo.assert_called_once()


# Additional Tests for Edge Cases


def test_do_algorithm_with_invalid_place_type(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
    caplog,
):
    caplog.set_level(logging.WARNING)

    # Mock load_templates to return templates for an invalid place type
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
    }

    # Mock get_place_categories to return categories that don't match
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat2"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter algorithm to return empty
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {}
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Execute
    available_places = algorithm_instance.do_algorithm()

    # Assertions
    assert available_places == []
    assert any("No filtered places for" in record.message for record in caplog.records)


def test_do_algorithm_handles_exception_in_load_templates(
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock load_templates to raise an exception
    mock_templates_repository.load_templates.side_effect = Exception(
        "Load templates failed"
    )

    # Create instance
    algorithm = GetAvailablePlaceTypesAlgorithm(
        playthrough_name="playthrough",
        father_place_template="father_template",
        father_place_type=TemplateType.ROOM,
        place_type=TemplateType.LOCATION,
        filter_places_by_categories_algorithm_factory=mock_filter_places_by_categories_algorithm_factory,
        place_manager_factory=mock_place_manager_factory,
        templates_repository=mock_templates_repository,
    )

    # Execute and assert exception is propagated
    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()
    assert "Load templates failed" in str(exc_info.value)


def test_do_algorithm_handles_exception_in_get_place_categories(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
    }

    # Mock get_place_categories to raise exception
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.side_effect = Exception(
        "Get categories failed"
    )
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Execute and assert exception is propagated
    with pytest.raises(Exception) as exc_info:
        algorithm_instance.do_algorithm()
    assert "Get categories failed" in str(exc_info.value)


def test_do_algorithm_handles_exception_in_filter_algorithm(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
    }

    # Mock get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter algorithm to raise exception
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.side_effect = Exception(
        "Filter algorithm failed"
    )
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Execute and assert exception is propagated
    with pytest.raises(Exception) as exc_info:
        algorithm_instance.do_algorithm()
    assert "Filter algorithm failed" in str(exc_info.value)


def test_do_algorithm_handles_exception_in_get_places_of_type(
    algorithm_instance,
    mock_filter_places_by_categories_algorithm_factory,
    mock_place_manager_factory,
    mock_templates_repository,
):
    # Mock load_templates
    mock_templates_repository.load_templates.return_value = {
        "place1": {"category": "cat1"},
    }

    # Mock get_place_categories
    mock_place_manager = MagicMock()
    mock_place_manager.get_place_categories.return_value = ["cat1"]
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock filter algorithm
    mock_filter_algorithm = MagicMock()
    mock_filter_algorithm.do_algorithm.return_value = {
        "place1": {"category": "cat1"},
    }
    mock_filter_places_by_categories_algorithm_factory.create_algorithm.return_value = (
        mock_filter_algorithm
    )

    # Mock get_places_of_type to raise exception
    mock_place_manager.get_places_of_type.side_effect = Exception("Get places failed")

    # Execute and assert exception is propagated
    with pytest.raises(Exception) as exc_info:
        algorithm_instance.do_algorithm()
    assert "Get places failed" in str(exc_info.value)
