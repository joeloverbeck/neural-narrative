from unittest.mock import Mock, create_autospec

import pytest

from src.maps.algorithms.get_area_info_algorithm import GetAreaInfoAlgorithm
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.data.get_area_info_algorithm_data import GetAreaInfoAlgorithmData
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory


@pytest.fixture
def mock_get_places_in_place_algorithm():
    return create_autospec(GetPlacesInPlaceAlgorithm)


@pytest.fixture
def mock_get_available_place_types_algorithm():
    return create_autospec(GetAvailablePlaceTypesAlgorithm)


@pytest.fixture
def mock_navigation_manager_factory():
    mock_factory = create_autospec(NavigationManagerFactory)
    mock_navigation_manager = Mock()
    mock_factory.create_navigation_manager.return_value = mock_navigation_manager
    return mock_factory, mock_navigation_manager


def test_init_success(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    factory, _ = mock_navigation_manager_factory

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    assert algorithm._playthrough_name == playthrough_name
    assert algorithm._current_place_identifier == current_place_identifier
    assert (
        algorithm._get_places_in_place_algorithm is mock_get_places_in_place_algorithm
    )
    assert (
        algorithm._get_available_place_types_algorithm
        is mock_get_available_place_types_algorithm
    )
    assert algorithm._navigation_manager_factory is factory


def test_init_empty_playthrough_name(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    with pytest.raises(ValueError) as exc_info:
        GetAreaInfoAlgorithm(
            playthrough_name="",
            current_place_identifier="Place123",
            get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
            get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
            navigation_manager_factory=mock_navigation_manager_factory[0],
        )
    assert "playthrough_name" in str(exc_info.value)


def test_init_empty_current_place_identifier(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    with pytest.raises(ValueError) as exc_info:
        GetAreaInfoAlgorithm(
            playthrough_name="TestPlaythrough",
            current_place_identifier="",
            get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
            get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
            navigation_manager_factory=mock_navigation_manager_factory[0],
        )
    assert "current_place_identifier" in str(exc_info.value)


def test_init_non_string_playthrough_name(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    with pytest.raises(ValueError) as exc_info:
        GetAreaInfoAlgorithm(
            playthrough_name=None,  # noqa
            current_place_identifier="Place123",
            get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
            get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
            navigation_manager_factory=mock_navigation_manager_factory[0],
        )
    assert "playthrough_name" in str(exc_info.value)


def test_init_non_string_current_place_identifier(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    with pytest.raises(TypeError) as exc_info:
        GetAreaInfoAlgorithm(
            playthrough_name="TestPlaythrough",
            current_place_identifier=123,  # noqa
            get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
            get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
            navigation_manager_factory=mock_navigation_manager_factory[0],
        )
    assert "current_place_identifier" in str(exc_info.value)


def test_do_algorithm_returns_correct_data(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = [
        "Location1",
        "Location2",
    ]
    mock_get_available_place_types_algorithm.do_algorithm.return_value = [
        "TypeA",
        "TypeB",
    ]
    factory, mock_navigation_manager = mock_navigation_manager_factory
    mock_navigation_manager.get_cardinal_connections.return_value = {
        "N": "PlaceN",
        "S": "PlaceS",
    }

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    result = algorithm.do_algorithm()

    # Assertions
    mock_get_places_in_place_algorithm.do_algorithm.assert_called_once()
    factory.create_navigation_manager.assert_called_once()
    mock_navigation_manager.get_cardinal_connections.assert_called_once_with(
        current_place_identifier
    )
    mock_get_available_place_types_algorithm.do_algorithm.assert_called_once()

    assert isinstance(result, GetAreaInfoAlgorithmData)
    assert result.locations_present == ["Location1", "Location2"]
    assert result.can_search_for_location is True
    assert result.available_location_types == ["TypeA", "TypeB"]
    assert result.cardinal_connections == {"N": "PlaceN", "S": "PlaceS"}


def test_can_search_for_location_false_when_no_available_types(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = ["Location1"]
    mock_get_available_place_types_algorithm.do_algorithm.return_value = []
    factory, mock_navigation_manager = mock_navigation_manager_factory
    mock_navigation_manager.get_cardinal_connections.return_value = {"E": "PlaceE"}

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    result = algorithm.do_algorithm()

    # Assertions
    assert result.can_search_for_location is False
    assert result.available_location_types == []


def test_do_algorithm_with_empty_locations_present(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = []
    mock_get_available_place_types_algorithm.do_algorithm.return_value = ["TypeA"]
    factory, mock_navigation_manager = mock_navigation_manager_factory
    mock_navigation_manager.get_cardinal_connections.return_value = {}

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    result = algorithm.do_algorithm()

    # Assertions
    assert result.locations_present == []
    assert result.can_search_for_location is True
    assert result.cardinal_connections == {}


def test_do_algorithm_no_cardinal_connections(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = ["Location1"]
    mock_get_available_place_types_algorithm.do_algorithm.return_value = ["TypeA"]
    factory, mock_navigation_manager = mock_navigation_manager_factory
    mock_navigation_manager.get_cardinal_connections.return_value = {}

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    result = algorithm.do_algorithm()

    # Assertions
    assert result.cardinal_connections == {}


def test_do_algorithm_dependencies_raise_exception(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks to raise exceptions
    mock_get_places_in_place_algorithm.do_algorithm.side_effect = Exception(
        "Error in get_places"
    )
    factory, _ = mock_navigation_manager_factory

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()

    assert "Error in get_places" in str(exc_info.value)


def test_do_algorithm_navigation_manager_factory_raises(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = ["Location1"]
    mock_get_available_place_types_algorithm.do_algorithm.return_value = ["TypeA"]
    factory, _ = mock_navigation_manager_factory
    factory.create_navigation_manager.side_effect = Exception(
        "Failed to create navigation manager"
    )

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()

    assert "Failed to create navigation manager" in str(exc_info.value)


def test_do_algorithm_available_place_types_none(
    mock_get_places_in_place_algorithm,
    mock_get_available_place_types_algorithm,
    mock_navigation_manager_factory,
):
    playthrough_name = "TestPlaythrough"
    current_place_identifier = "Place123"

    # Setup mocks
    mock_get_places_in_place_algorithm.do_algorithm.return_value = ["Location1"]
    mock_get_available_place_types_algorithm.do_algorithm.return_value = None
    factory, mock_navigation_manager = mock_navigation_manager_factory
    mock_navigation_manager.get_cardinal_connections.return_value = {"W": "PlaceW"}

    algorithm = GetAreaInfoAlgorithm(
        playthrough_name=playthrough_name,
        current_place_identifier=current_place_identifier,
        get_places_in_place_algorithm=mock_get_places_in_place_algorithm,
        get_available_place_types_algorithm=mock_get_available_place_types_algorithm,
        navigation_manager_factory=factory,
    )

    result = algorithm.do_algorithm()

    # Assertions
    assert result.can_search_for_location is False
    assert result.available_location_types is None
