# tests/test_get_place_info_algorithm.py

from unittest.mock import MagicMock, create_autospec

import pytest

from src.base.enums import TemplateType
from src.maps.algorithms.get_area_info_algorithm import GetAreaInfoAlgorithm
from src.maps.algorithms.get_location_info_algorithm import GetLocationInfoAlgorithm
from src.maps.algorithms.get_place_info_algorithm import GetPlaceInfoAlgorithm
from src.maps.data.get_place_info_algorithm_data import GetPlaceInfoAlgorithmData
from src.maps.factories.place_manager_factory import PlaceManagerFactory


@pytest.fixture
def mock_get_area_info_algorithm():
    return create_autospec(GetAreaInfoAlgorithm)


@pytest.fixture
def mock_get_location_info_algorithm():
    return create_autospec(GetLocationInfoAlgorithm)


@pytest.fixture
def mock_place_manager_factory():
    return create_autospec(PlaceManagerFactory)


@pytest.fixture
def get_place_info_algorithm(
    mock_get_area_info_algorithm,
    mock_get_location_info_algorithm,
    mock_place_manager_factory,
):
    return GetPlaceInfoAlgorithm(
        get_area_info_algorithm=mock_get_area_info_algorithm,
        get_location_info_algorithm=mock_get_location_info_algorithm,
        place_manager_factory=mock_place_manager_factory,
    )


def test_do_algorithm_area_type(
    get_place_info_algorithm,
    mock_get_area_info_algorithm,
    mock_get_location_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock the data returned by GetAreaInfoAlgorithm
    area_data = GetPlaceInfoAlgorithmData(
        locations_present=[{"id": 1, "name": "Location A"}],
        can_search_for_location=True,
        available_location_types=["Type1", "Type2"],
        cardinal_connections={"north": {"connected_to": "Location B"}},
        rooms_present=None,
        can_search_for_room=False,
        available_room_types=[],
    )
    # Adjust the data to only include area-related fields
    area_algorithm_data = MagicMock(spec=GetPlaceInfoAlgorithmData)
    area_algorithm_data.locations_present = area_data.locations_present
    area_algorithm_data.can_search_for_location = area_data.can_search_for_location
    area_algorithm_data.available_location_types = area_data.available_location_types
    area_algorithm_data.cardinal_connections = area_data.cardinal_connections
    # Ensure other fields are set to default values
    area_algorithm_data.rooms_present = area_data.rooms_present
    area_algorithm_data.can_search_for_room = area_data.can_search_for_room
    area_algorithm_data.available_room_types = area_data.available_room_types

    mock_get_area_info_algorithm.do_algorithm.return_value = area_algorithm_data

    # Act
    result = get_place_info_algorithm.do_algorithm()

    # Assert
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_get_area_info_algorithm.do_algorithm.assert_called_once()
    mock_get_location_info_algorithm.do_algorithm.assert_not_called()

    assert result.locations_present == area_data.locations_present
    assert result.can_search_for_location == area_data.can_search_for_location
    assert result.available_location_types == area_data.available_location_types
    assert result.cardinal_connections == area_data.cardinal_connections

    # Fields not set by AREA type
    assert result.rooms_present is None
    assert result.can_search_for_room is False
    assert result.available_room_types == []


def test_do_algorithm_location_type(
    get_place_info_algorithm,
    mock_get_location_info_algorithm,
    mock_get_area_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock the data returned by GetLocationInfoAlgorithm
    location_data = GetPlaceInfoAlgorithmData(
        locations_present=None,
        can_search_for_location=False,
        available_location_types=[],
        cardinal_connections=None,
        rooms_present=[{"id": 101, "name": "Room A"}],
        can_search_for_room=True,
        available_room_types=["RoomType1", "RoomType2"],
    )
    # Adjust the data to only include location-related fields
    location_algorithm_data = MagicMock(spec=GetPlaceInfoAlgorithmData)
    location_algorithm_data.rooms_present = location_data.rooms_present
    location_algorithm_data.can_search_for_room = location_data.can_search_for_room
    location_algorithm_data.available_room_types = location_data.available_room_types
    # Ensure other fields are set to default values
    location_algorithm_data.locations_present = location_data.locations_present
    location_algorithm_data.can_search_for_location = (
        location_data.can_search_for_location
    )
    location_algorithm_data.available_location_types = (
        location_data.available_location_types
    )
    location_algorithm_data.cardinal_connections = location_data.cardinal_connections

    mock_get_location_info_algorithm.do_algorithm.return_value = location_algorithm_data

    # Act
    result = get_place_info_algorithm.do_algorithm()

    # Assert
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_get_location_info_algorithm.do_algorithm.assert_called_once()
    mock_get_area_info_algorithm.do_algorithm.assert_not_called()

    assert result.rooms_present == location_data.rooms_present
    assert result.can_search_for_room == location_data.can_search_for_room
    assert result.available_room_types == location_data.available_room_types

    # Fields not set by LOCATION type
    assert result.locations_present is None
    assert result.can_search_for_location is False
    assert result.available_location_types == []
    assert result.cardinal_connections is None


def test_do_algorithm_other_template_type(
    get_place_info_algorithm,
    mock_get_area_info_algorithm,
    mock_get_location_info_algorithm,
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.REGION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Act
    result = get_place_info_algorithm.do_algorithm()

    # Assert
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_get_area_info_algorithm.do_algorithm.assert_not_called()
    mock_get_location_info_algorithm.do_algorithm.assert_not_called()

    # All fields should be default or None
    assert result.locations_present is None
    assert result.can_search_for_location is False
    assert result.available_location_types == []
    assert result.cardinal_connections is None
    assert result.rooms_present is None
    assert result.can_search_for_room is False
    assert result.available_room_types == []


def test_do_algorithm_area_type_with_empty_data(
    get_place_info_algorithm,
    mock_get_area_info_algorithm,
    mock_get_location_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock empty data returned by GetAreaInfoAlgorithm
    area_algorithm_data = MagicMock(spec=GetPlaceInfoAlgorithmData)
    area_algorithm_data.locations_present = []
    area_algorithm_data.can_search_for_location = False
    area_algorithm_data.available_location_types = []
    area_algorithm_data.cardinal_connections = {}
    area_algorithm_data.rooms_present = None
    area_algorithm_data.can_search_for_room = False
    area_algorithm_data.available_room_types = []

    mock_get_area_info_algorithm.do_algorithm.return_value = area_algorithm_data

    # Act
    result = get_place_info_algorithm.do_algorithm()

    # Assert
    mock_get_area_info_algorithm.do_algorithm.assert_called_once()

    assert result.locations_present == []
    assert result.can_search_for_location is False
    assert result.available_location_types == []
    assert result.cardinal_connections == {}

    # Fields not set by AREA type
    assert result.rooms_present is None
    assert result.can_search_for_room is False
    assert result.available_room_types == []


def test_do_algorithm_location_type_with_empty_data(
    get_place_info_algorithm,
    mock_get_location_info_algorithm,
    mock_get_area_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Mock empty data returned by GetLocationInfoAlgorithm
    location_algorithm_data = MagicMock(spec=GetPlaceInfoAlgorithmData)
    location_algorithm_data.rooms_present = []
    location_algorithm_data.can_search_for_room = False
    location_algorithm_data.available_room_types = []
    location_algorithm_data.locations_present = None
    location_algorithm_data.can_search_for_location = False
    location_algorithm_data.available_location_types = []
    location_algorithm_data.cardinal_connections = None

    mock_get_location_info_algorithm.do_algorithm.return_value = location_algorithm_data

    # Act
    result = get_place_info_algorithm.do_algorithm()

    # Assert
    mock_get_location_info_algorithm.do_algorithm.assert_called_once()

    assert result.rooms_present == []
    assert result.can_search_for_room is False
    assert result.available_room_types == []

    # Fields not set by LOCATION type
    assert result.locations_present is None
    assert result.can_search_for_location is False
    assert result.available_location_types == []
    assert result.cardinal_connections is None


def test_do_algorithm_area_type_algorithm_exception(
    get_place_info_algorithm,
    mock_get_area_info_algorithm,
    mock_get_location_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Configure the GetAreaInfoAlgorithm to raise an exception
    mock_get_area_info_algorithm.do_algorithm.side_effect = Exception("Algorithm error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_place_info_algorithm.do_algorithm()

    assert "Algorithm error" in str(exc_info.value)
    mock_get_area_info_algorithm.do_algorithm.assert_called_once()


def test_do_algorithm_location_type_algorithm_exception(
    get_place_info_algorithm,
    mock_get_location_info_algorithm,
    mock_get_area_info_algorithm,  # Added this fixture
    mock_place_manager_factory,
):
    # Arrange
    mock_place_manager = MagicMock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager

    # Configure the GetLocationInfoAlgorithm to raise an exception
    mock_get_location_info_algorithm.do_algorithm.side_effect = Exception(
        "Algorithm error"
    )

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_place_info_algorithm.do_algorithm()

    assert "Algorithm error" in str(exc_info.value)
    mock_get_location_info_algorithm.do_algorithm.assert_called_once()
