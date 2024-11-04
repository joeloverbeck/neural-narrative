from unittest.mock import Mock, patch

import pytest

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.algorithms.get_current_area_identifier_algorithm import (
    GetCurrentAreaIdentifierAlgorithm,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


@pytest.fixture
def mock_place_manager_factory():
    return Mock(spec=PlaceManagerFactory)


@pytest.fixture
def mock_playthrough_manager():
    return Mock(spec=PlaythroughManager)


@pytest.fixture
def mock_map_repository():
    return Mock(spec=MapRepository)


@pytest.fixture
def mock_place_manager():
    return Mock()


def test_initialization_with_all_dependencies(
    mock_place_manager_factory, mock_playthrough_manager, mock_map_repository
):
    playthrough_name = "test_playthrough"
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    assert algorithm._place_manager_factory == mock_place_manager_factory
    assert algorithm._playthrough_manager == mock_playthrough_manager
    assert algorithm._map_repository == mock_map_repository


def test_initialization_with_default_dependencies(
    mock_place_manager_factory, mock_playthrough_manager
):
    playthrough_name = "test_playthrough"

    with patch(
        "src.maps.algorithms.get_current_area_identifier_algorithm.PlaythroughManager"
    ) as MockPlaythroughManager, patch(
        "src.maps.algorithms.get_current_area_identifier_algorithm.MapRepository"
    ) as MockMapRepository:

        algorithm = GetCurrentAreaIdentifierAlgorithm(
            playthrough_name=playthrough_name,
            place_manager_factory=mock_place_manager_factory,
        )

        MockPlaythroughManager.assert_called_once_with(playthrough_name)
        MockMapRepository.assert_called_once_with(playthrough_name)

        assert algorithm._playthrough_manager == MockPlaythroughManager.return_value
        assert algorithm._map_repository == MockMapRepository.return_value


@pytest.mark.parametrize(
    "current_place_type, expected_identifier",
    [
        (TemplateType.AREA, "area_123"),
    ],
)
def test_do_algorithm_area(
    current_place_type,
    expected_identifier,
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        expected_identifier
    )

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    assert result == expected_identifier
    mock_map_repository.load_map_data.assert_not_called()


@pytest.mark.parametrize(
    "current_place_type, current_place_identifier, map_data, expected_identifier",
    [
        (
            TemplateType.LOCATION,
            "location_456",
            {"location_456": {"area": "area_123"}},
            "area_123",
        ),
    ],
)
def test_do_algorithm_location(
    current_place_type,
    current_place_identifier,
    map_data,
    expected_identifier,
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    mock_map_repository.load_map_data.return_value = map_data

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    assert result == expected_identifier
    mock_map_repository.load_map_data.assert_called_once()


@pytest.mark.parametrize(
    "current_place_type, current_place_identifier, map_data, expected_identifier",
    [
        (
            TemplateType.ROOM,
            "room_789",
            {
                "room_789": {"location": "location_456"},
                "location_456": {"area": "area_123"},
            },
            "area_123",
        ),
    ],
)
def test_do_algorithm_room(
    current_place_type,
    current_place_identifier,
    map_data,
    expected_identifier,
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    mock_map_repository.load_map_data.return_value = map_data

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algorithm.do_algorithm()

    assert result == expected_identifier
    # load_map_data should be called twice in ROOM case
    assert mock_map_repository.load_map_data.call_count == 2


def test_do_algorithm_unsupported_type(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"
    unsupported_type = TemplateType.WORLD
    current_place_identifier = "world_001"

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = unsupported_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()

    assert (
        str(exc_info.value)
        == f"Not handled for current place type '{unsupported_type}'."
    )
    mock_map_repository.load_map_data.assert_called_once()


def test_do_algorithm_location_missing_parent_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"
    current_place_type = TemplateType.LOCATION
    current_place_identifier = "location_456"
    map_data = {"location_456": {"invalid_key": "area_123"}}  # Missing 'area' key

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    mock_map_repository.load_map_data.return_value = map_data

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algorithm.do_algorithm()

    assert exc_info.value.args[0] == "area"


def test_do_algorithm_room_missing_location_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"
    current_place_type = TemplateType.ROOM
    current_place_identifier = "room_789"
    map_data = {
        "room_789": {"invalid_key": "location_456"},  # Missing 'location' key
        "location_456": {"area": "area_123"},
    }

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    mock_map_repository.load_map_data.return_value = map_data

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algorithm.do_algorithm()

    assert exc_info.value.args[0] == "location"


def test_do_algorithm_room_missing_area_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    mock_place_manager,
):
    playthrough_name = "test_playthrough"
    current_place_type = TemplateType.ROOM
    current_place_identifier = "room_789"
    map_data = {
        "room_789": {"location": "location_456"},
        "location_456": {"invalid_key": "area_123"},  # Missing 'area' key
    }

    # Setup mocks
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = current_place_type
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )
    mock_map_repository.load_map_data.return_value = map_data

    # Initialize algorithm
    algorithm = GetCurrentAreaIdentifierAlgorithm(
        playthrough_name=playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algorithm.do_algorithm()

    assert exc_info.value.args[0] == "area"


def test_initialization_with_empty_playthrough_name():
    playthrough_name = ""

    with patch(
        "src.maps.algorithms.get_current_area_identifier_algorithm.validate_non_empty_string"
    ) as mock_validate:
        mock_validate.side_effect = ValueError("playthrough_name cannot be empty")

        with pytest.raises(ValueError) as exc_info:
            GetCurrentAreaIdentifierAlgorithm(
                playthrough_name=playthrough_name,
                place_manager_factory=Mock(spec=PlaceManagerFactory),
            )

        mock_validate.assert_called_once_with(playthrough_name, "playthrough_name")
        assert str(exc_info.value) == "playthrough_name cannot be empty"
