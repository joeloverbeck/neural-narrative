from unittest.mock import Mock, patch

import pytest

# Assuming the following imports based on the provided code
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.algorithms.get_current_area_algorithm import GetCurrentAreaAlgorithm
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


# Fixtures for common mocks
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
def valid_playthrough_name():
    return "test_playthrough"


@pytest.fixture
def default_map_file():
    return {
        "area_1": {"name": "Area 1"},
        "location_1": {"name": "Location 1", "area": "area_1"},
        "room_1": {"name": "Room 1", "location": "location_1"},
    }


# Initialization Tests
def test_initialization_with_required_parameters(
    mock_place_manager_factory, valid_playthrough_name
):
    with patch(
        "src.maps.algorithms.get_current_area_algorithm.MapRepository"
    ) as mock_map_repo_cls, patch(
        "src.maps.algorithms.get_current_area_algorithm.PlaythroughManager"
    ) as mock_playthrough_mgr_cls:
        instance = GetCurrentAreaAlgorithm(
            playthrough_name=valid_playthrough_name,
            place_manager_factory=mock_place_manager_factory,
        )
        mock_playthrough_mgr_cls.assert_called_once_with(valid_playthrough_name)
        mock_map_repo_cls.assert_called_once_with(valid_playthrough_name)
        assert instance._place_manager_factory == mock_place_manager_factory


def test_initialization_with_all_parameters(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
):
    instance = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )
    assert instance._place_manager_factory == mock_place_manager_factory
    assert instance._playthrough_manager == mock_playthrough_manager
    assert instance._map_repository == mock_map_repository


def test_initialization_with_empty_playthrough_name(mock_place_manager_factory):
    with pytest.raises(ValueError) as exc_info:
        GetCurrentAreaAlgorithm(
            playthrough_name="", place_manager_factory=mock_place_manager_factory
        )
    assert "playthrough_name" in str(exc_info.value)


# do_algorithm Tests for TemplateType.AREA
def test_do_algorithm_area(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "area_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algo.do_algorithm()

    assert result == default_map_file["area_1"]
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()


# do_algorithm Tests for TemplateType.LOCATION
def test_do_algorithm_location(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "location_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algo.do_algorithm()

    assert result == default_map_file["area_1"]
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()


# do_algorithm Tests for TemplateType.ROOM
def test_do_algorithm_room(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.ROOM
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "room_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algo.do_algorithm()

    assert result == default_map_file["area_1"]
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()


# do_algorithm Tests for Unsupported TemplateType
def test_do_algorithm_unsupported_template_type(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = (
        TemplateType.WORLD
    )  # Unsupported
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "world_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(ValueError) as exc_info:
        algo.do_algorithm()

    assert "Not handled for current place type" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()


# Edge Case Tests: Missing keys in map_file for AREA
def test_do_algorithm_area_missing_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = {}
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "area_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algo.do_algorithm()

    assert "area_1" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Edge Case Tests: Missing parent key for LOCATION
def test_do_algorithm_location_missing_parent_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Modify map_file to remove parent key for location
    modified_map_file = {
        "location_1": {"name": "Location 1"},  # Missing 'area'
    }

    mock_map_repository.load_map_data.return_value = modified_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.LOCATION
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "location_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algo.do_algorithm()

    assert "area" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Edge Case Tests: Missing parent key for ROOM
def test_do_algorithm_room_missing_parent_keys(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    # Modify map_file to remove parent keys
    modified_map_file = {
        "room_1": {"name": "Room 1"},  # Missing 'location'
    }

    mock_map_repository.load_map_data.return_value = modified_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.ROOM
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "room_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algo.do_algorithm()

    assert "location" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Edge Case Tests: Deeply nested missing area for ROOM
def test_do_algorithm_room_missing_area_key(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
):
    # Setup map_file where room points to location, but location lacks area
    map_file = {
        "room_1": {"name": "Room 1", "location": "location_1"},
        "location_1": {"name": "Location 1"},  # Missing 'area'
    }

    mock_map_repository.load_map_data.return_value = map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.ROOM
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "room_1"

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(KeyError) as exc_info:
        algo.do_algorithm()

    assert "area" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Dependency Tests: Ensure PlaythroughManager and MapRepository are instantiated correctly
def test_dependencies_instantiated_correctly(
    mock_place_manager_factory, valid_playthrough_name
):
    with patch(
        "src.maps.algorithms.get_current_area_algorithm.MapRepository"
    ) as mock_map_repo_cls, patch(
        "src.maps.algorithms.get_current_area_algorithm.PlaythroughManager"
    ) as mock_playthrough_mgr_cls:
        GetCurrentAreaAlgorithm(
            playthrough_name=valid_playthrough_name,
            place_manager_factory=mock_place_manager_factory,
        )
        mock_playthrough_mgr_cls.assert_called_once_with(valid_playthrough_name)
        mock_map_repo_cls.assert_called_once_with(valid_playthrough_name)


# Dependency Tests: Ensure PlaceManagerFactory.create_place_manager is called
def test_place_manager_creation(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "area_1"

    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    algo.do_algorithm()

    mock_place_manager_factory.create_place_manager.assert_called_once()


# Error Handling Tests: MapRepository.load_map_data raises exception
def test_do_algorithm_map_repository_exception(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
):
    mock_map_repository.load_map_data.side_effect = Exception("Load error")
    mock_place_manager = Mock()
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_place_manager.get_current_place_type.return_value = TemplateType.AREA
    mock_playthrough_manager.get_current_place_identifier.return_value = "area_1"

    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(Exception) as exc_info:
        algo.do_algorithm()

    assert "Load error" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()


# Error Handling Tests: PlaceManager.get_current_place_type raises exception
def test_do_algorithm_place_manager_exception(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
):
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.side_effect = Exception(
        "Place type error"
    )
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    mock_playthrough_manager.get_current_place_identifier.return_value = "area_1"

    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    with pytest.raises(Exception) as exc_info:
        algo.do_algorithm()

    assert "Place type error" in str(exc_info.value)
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()


# Parameterized Tests for Different TemplateTypes
@pytest.mark.parametrize(
    "template_type,expected_result_key",
    [
        (TemplateType.AREA, "area_1"),
        (TemplateType.LOCATION, "area_1"),
        (TemplateType.ROOM, "area_1"),
    ],
)
def test_do_algorithm_parameterized(
    mock_place_manager_factory,
    mock_playthrough_manager,
    mock_map_repository,
    valid_playthrough_name,
    default_map_file,
    template_type,
    expected_result_key,
):
    # Setup mocks
    mock_map_repository.load_map_data.return_value = default_map_file
    mock_place_manager = Mock()
    mock_place_manager.get_current_place_type.return_value = template_type
    mock_place_manager_factory.create_place_manager.return_value = mock_place_manager
    current_place_identifier = {
        TemplateType.AREA: "area_1",
        TemplateType.LOCATION: "location_1",
        TemplateType.ROOM: "room_1",
    }[template_type]
    mock_playthrough_manager.get_current_place_identifier.return_value = (
        current_place_identifier
    )

    # Initialize the algorithm
    algo = GetCurrentAreaAlgorithm(
        playthrough_name=valid_playthrough_name,
        place_manager_factory=mock_place_manager_factory,
        playthrough_manager=mock_playthrough_manager,
        map_repository=mock_map_repository,
    )

    result = algo.do_algorithm()

    assert result == default_map_file[expected_result_key]
    mock_map_repository.load_map_data.assert_called_once()
    mock_place_manager_factory.create_place_manager.assert_called_once()
    mock_place_manager.get_current_place_type.assert_called_once()
    mock_playthrough_manager.get_current_place_identifier.assert_called_once()
