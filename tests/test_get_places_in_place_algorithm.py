import logging
from unittest.mock import patch

import pytest

from src.base.enums import TemplateType
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm


# Mocking the validate_non_empty_string function
@pytest.fixture
def mock_validate_non_empty_string():
    with patch(
        "src.maps.algorithms.get_places_in_place_algorithm.validate_non_empty_string"
    ) as mock_validate:
        yield mock_validate


# Mocking the MapRepository class
@pytest.fixture
def mock_map_repository():
    with patch(
        "src.maps.algorithms.get_places_in_place_algorithm.MapRepository"
    ) as MockMapRepo:
        instance = MockMapRepo.return_value
        yield instance


# Test Initialization with empty playthrough_name
def test_initialization_empty_playthrough_name(mock_validate_non_empty_string):
    with pytest.raises(ValueError):
        mock_validate_non_empty_string.side_effect = ValueError(
            "playthrough_name cannot be empty"
        )
        GetPlacesInPlaceAlgorithm(
            playthrough_name="",
            containing_place_identifier="Place123",
            containing_place_type=TemplateType.ROOM,
            contained_place_type=TemplateType.LOCATION,
        )
    mock_validate_non_empty_string.assert_called_with("", "playthrough_name")


# Test do_algorithm with matching contained places
def test_do_algorithm_with_matches(mock_map_repository):
    mock_map_repository.load_map_data.return_value = {
        "Place1": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateA",
        },
        "Place2": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateB",
        },
        "Place3": {
            "room": "Place456",
            "type": "location",
            "place_template": "TemplateC",
        },
        "Place4": {
            "room": "Place123",
            "type": "area",
            "place_template": "TemplateD",
        },
    }

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    expected = [
        {"identifier": "Place1", "place_template": "TemplateA"},
        {"identifier": "Place2", "place_template": "TemplateB"},
    ]

    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


# Test do_algorithm with different TemplateTypes
@pytest.mark.parametrize(
    "containing_type, contained_type, map_data, expected",
    [
        (
            TemplateType.LOCATION,
            TemplateType.AREA,
            {
                "Place1": {
                    "location": "Loc123",
                    "type": "area",
                    "place_template": "TemplateA",
                },
                "Place2": {
                    "location": "Loc123",
                    "type": "story_universe",
                    "place_template": "TemplateB",
                },
            },
            [{"identifier": "Place1", "place_template": "TemplateA"}],
        ),
        (
            TemplateType.AREA,
            TemplateType.REGION,
            {
                "Place1": {
                    "area": "Area456",
                    "type": "region",
                    "place_template": "TemplateC",
                },
                "Place2": {
                    "area": "Area456",
                    "type": "world",
                    "place_template": "TemplateD",
                },
            },
            [{"identifier": "Place1", "place_template": "TemplateC"}],
        ),
    ],
)
def test_do_algorithm_various_template_types(
    mock_map_repository, containing_type, contained_type, map_data, expected
):
    mock_map_repository.load_map_data.return_value = map_data

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier=(
            "Loc123" if containing_type == TemplateType.LOCATION else "Area456"
        ),
        containing_place_type=containing_type,
        contained_place_type=contained_type,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


# Test using default MapRepository when none is provided
def test_do_algorithm_default_map_repository(mock_validate_non_empty_string):
    with patch(
        "src.maps.algorithms.get_places_in_place_algorithm.MapRepository"
    ) as MockMapRepo:
        instance = MockMapRepo.return_value
        instance.load_map_data.return_value = {
            "Place1": {
                "room": "Place123",
                "type": "location",
                "place_template": "TemplateA",
            }
        }

        algorithm = GetPlacesInPlaceAlgorithm(
            playthrough_name="DefaultRepoPlaythrough",
            containing_place_identifier="Place123",
            containing_place_type=TemplateType.ROOM,
            contained_place_type=TemplateType.LOCATION,
        )

        result = algorithm.do_algorithm()

        expected = [{"identifier": "Place1", "place_template": "TemplateA"}]
        assert result == expected
        MockMapRepo.assert_called_once_with("DefaultRepoPlaythrough")
        instance.load_map_data.assert_called_once()


# Test do_algorithm when load_map_data raises an exception
def test_do_algorithm_load_map_data_exception(mock_map_repository, caplog):
    mock_map_repository.load_map_data.side_effect = Exception("Failed to load map data")

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()

    assert str(exc_info.value) == "Failed to load map data"
    mock_map_repository.load_map_data.assert_called_once()


# Test logging when matches are found (no warning should be logged)
def test_do_algorithm_with_matches_no_warning(mock_map_repository, caplog):
    mock_map_repository.load_map_data.return_value = {
        "Place1": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateA",
        }
    }

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    with caplog.at_level(logging.WARNING):
        result = algorithm.do_algorithm()

    assert result == [{"identifier": "Place1", "place_template": "TemplateA"}]
    mock_map_repository.load_map_data.assert_called_once()
    # Ensure no warnings were logged
    warnings = [
        record for record in caplog.records if record.levelno == logging.WARNING
    ]
    assert not warnings


# Test that place_template can be None
def test_do_algorithm_place_template_none(mock_map_repository):
    mock_map_repository.load_map_data.return_value = {
        "Place1": {
            "room": "Place123",
            "type": "location",
            "place_template": None,
        }
    }

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    expected = [{"identifier": "Place1", "place_template": None}]
    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


# Test with multiple contained_place_types
def test_do_algorithm_multiple_contained_types(mock_map_repository):
    mock_map_repository.load_map_data.return_value = {
        "Place1": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateA",
        },
        "Place2": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateB",
        },
        "Place3": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateC",
        },
    }

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    expected = [
        {"identifier": "Place1", "place_template": "TemplateA"},
        {"identifier": "Place2", "place_template": "TemplateB"},
        {"identifier": "Place3", "place_template": "TemplateC"},
    ]

    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


# Test with additional irrelevant data in map entries
def test_do_algorithm_irrelevant_data(mock_map_repository):
    mock_map_repository.load_map_data.return_value = {
        "Place1": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateA",
            "extra_field": "ExtraData1",
        },
        "Place2": {
            "room": "Place123",
            "type": "location",
            "place_template": "TemplateB",
            "extra_field": "ExtraData2",
        },
    }

    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="Place123",
        containing_place_type=TemplateType.ROOM,
        contained_place_type=TemplateType.LOCATION,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    expected = [
        {"identifier": "Place1", "place_template": "TemplateA"},
        {"identifier": "Place2", "place_template": "TemplateB"},
    ]

    assert result == expected
    mock_map_repository.load_map_data.assert_called_once()


# Test with various containing_place_types and contained_place_types
@pytest.mark.parametrize(
    "containing_type, contained_type",
    [
        (TemplateType.WORLD, TemplateType.STORY_UNIVERSE),
        (TemplateType.REGION, TemplateType.AREA),
        (TemplateType.AREA, TemplateType.ROOM),
    ],
)
def test_initialization_various_template_types(
    containing_type, contained_type, mock_validate_non_empty_string, mock_map_repository
):
    algorithm = GetPlacesInPlaceAlgorithm(
        playthrough_name="TestPlaythrough",
        containing_place_identifier="PlaceXYZ",
        containing_place_type=containing_type,
        contained_place_type=contained_type,
        map_repository=mock_map_repository,
    )

    mock_validate_non_empty_string.assert_any_call(
        "TestPlaythrough", "playthrough_name"
    )
    mock_validate_non_empty_string.assert_any_call(
        "PlaceXYZ", "containing_place_identifier"
    )
    assert algorithm._containing_place_type == containing_type
    assert algorithm._contained_place_type == contained_type
