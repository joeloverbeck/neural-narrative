from unittest.mock import MagicMock

import pytest

from src.maps.enums import CardinalDirection
from src.maps.map_repository import MapRepository
from src.maps.navigation_manager import NavigationManager


def test_does_area_have_cardinal_connection_true():
    map_data = {"area1": {"type": "area", "north": "area2"}, "area2": {"type": "area"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    cardinal_direction = CardinalDirection.NORTH
    result = nav_manager.does_area_have_cardinal_connection(
        area_identifier, cardinal_direction
    )
    assert result is True


def test_does_area_have_cardinal_connection_false():
    map_data = {"area1": {"type": "area"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    cardinal_direction = CardinalDirection.SOUTH
    result = nav_manager.does_area_have_cardinal_connection(
        area_identifier, cardinal_direction
    )
    assert result is False


def test_does_area_have_cardinal_connection_invalid_area():
    map_data = {"area1": {"type": "area"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "invalid_area"
    cardinal_direction = CardinalDirection.NORTH
    with pytest.raises(ValueError, match="'invalid_area' is not a valid area."):
        nav_manager.does_area_have_cardinal_connection(
            area_identifier, cardinal_direction
        )


def test_does_area_have_cardinal_connection_invalid_type():
    map_data = {"area1": {"type": "location"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    cardinal_direction = CardinalDirection.EAST
    with pytest.raises(ValueError, match="'area1' is not a valid area."):
        nav_manager.does_area_have_cardinal_connection(
            area_identifier, cardinal_direction
        )


def test_get_cardinal_connections_success():
    map_data = {
        "area1": {"type": "area", "north": "area2", "south": "area3"},
        "area2": {"type": "area", "place_template": "template2"},
        "area3": {"type": "area"},
    }
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    with pytest.raises(
        ValueError, match="Place template not found for connected area 'area3'."
    ):
        nav_manager.get_cardinal_connections(area_identifier)


def test_get_cardinal_connections_area_not_found():
    map_data = {}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    with pytest.raises(ValueError, match="Area identifier 'area1' not found in map."):
        nav_manager.get_cardinal_connections(area_identifier)


def test_get_cardinal_connections_invalid_type():
    map_data = {"area1": {"type": "location"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    with pytest.raises(
        ValueError,
        match="The given identifier 'area1' is not an area, but a 'location'.",
    ):
        nav_manager.get_cardinal_connections(area_identifier)


def test_get_cardinal_connections_missing_connected_area():
    map_data = {"area1": {"type": "area", "north": "area2"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    result = nav_manager.get_cardinal_connections(area_identifier)
    assert result["north"] is None
    assert result["south"] is None
    assert result["east"] is None
    assert result["west"] is None


def test_get_cardinal_connections_missing_place_template():
    map_data = {"area1": {"type": "area", "north": "area2"}, "area2": {"type": "area"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    area_identifier = "area1"
    with pytest.raises(
            ValueError, match="Place template not found for connected area 'area2'."
    ):
        nav_manager.get_cardinal_connections(area_identifier)


def test_create_cardinal_connection_success():
    map_data = {"area1": {"type": "area"}, "area2": {"type": "area"}}
    expected_map_data = {
        "area1": {"type": "area", "north": "area2"},
        "area2": {"type": "area"},
    }
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data.copy()
    nav_manager = NavigationManager(map_repository)
    cardinal_direction = CardinalDirection.NORTH
    origin_identifier = "area1"
    destination_identifier = "area2"
    nav_manager.create_cardinal_connection(
        cardinal_direction, origin_identifier, destination_identifier
    )
    map_repository.save_map_data.assert_called_once_with(expected_map_data)


def test_create_cardinal_connection_already_exists():
    map_data = {"area1": {"type": "area", "north": "area2"}}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    cardinal_direction = CardinalDirection.NORTH
    origin_identifier = "area1"
    destination_identifier = "area3"
    with pytest.raises(
        ValueError,
        match="There was already a cardinal connection for 'north' in 'area1'.",
    ):
        nav_manager.create_cardinal_connection(
            cardinal_direction, origin_identifier, destination_identifier
        )


def test_create_cardinal_connection_origin_missing():
    map_data = {}
    map_repository = MagicMock(spec=MapRepository)
    map_repository.load_map_data.return_value = map_data
    nav_manager = NavigationManager(map_repository)
    cardinal_direction = CardinalDirection.EAST
    origin_identifier = "area1"
    destination_identifier = "area2"
    with pytest.raises(KeyError):
        nav_manager.create_cardinal_connection(
            cardinal_direction, origin_identifier, destination_identifier
        )


def test_get_opposite_cardinal_direction_north():
    assert (
        NavigationManager.get_opposite_cardinal_direction(CardinalDirection.NORTH)
        == CardinalDirection.SOUTH
    )


def test_get_opposite_cardinal_direction_south():
    assert (
        NavigationManager.get_opposite_cardinal_direction(CardinalDirection.SOUTH)
        == CardinalDirection.NORTH
    )


def test_get_opposite_cardinal_direction_east():
    assert (
        NavigationManager.get_opposite_cardinal_direction(CardinalDirection.EAST)
        == CardinalDirection.WEST
    )


def test_get_opposite_cardinal_direction_west():
    assert (
        NavigationManager.get_opposite_cardinal_direction(CardinalDirection.WEST)
        == CardinalDirection.EAST
    )
