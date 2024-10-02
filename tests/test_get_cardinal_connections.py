from unittest.mock import MagicMock, patch

import pytest

from src.maps.map_manager import MapManager


def test_get_cardinal_connections_with_empty_identifier():
    """
    Test case where area_identifier is empty.
    Expected to raise ValueError.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    with pytest.raises(ValueError) as excinfo:
        map_manager.get_cardinal_connections("")
    assert "area_identifier can't be empty." in str(excinfo.value)


def test_get_cardinal_connections_with_nonexistent_identifier():
    """
    Test case where area_identifier does not exist in the map.
    Expected to raise ValueError.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(return_value={})
    with pytest.raises(ValueError) as excinfo:
        map_manager.get_cardinal_connections("nonexistent_area")
    assert "Area identifier 'nonexistent_area' not found in map." in str(excinfo.value)


def test_get_cardinal_connections_with_wrong_type():
    """
    Test case where area_identifier exists but is not of type 'area'.
    Expected to raise ValueError.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(
        return_value={"1": {"type": "region", "place_template": "Quixotania"}}
    )
    with pytest.raises(ValueError) as excinfo:
        map_manager.get_cardinal_connections("1")
    assert "The given identifier '1' is not an area, but a 'region'." in str(
        excinfo.value
    )


def test_get_cardinal_connections_with_partial_connections():
    """
    Test case where area has connections in some directions, but not others.
    Expected to return a dictionary with some directions set to None.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(
        return_value={
            "2": {
                "type": "area",
                "place_template": "Wonderwhirl Vale",
                "region": "1",
                "north": "4",
                "east": "5",
            },
            "4": {"type": "area", "place_template": "Northern Area", "region": "1"},
            "5": {"type": "area", "place_template": "Eastern Area", "region": "1"},
        }
    )
    expected_result = {
        "north": {"identifier": "4", "place_template": "Northern Area"},
        "south": None,
        "east": {"identifier": "5", "place_template": "Eastern Area"},
        "west": None,
    }
    result = map_manager.get_cardinal_connections("2")
    assert result == expected_result


def test_get_cardinal_connections_with_missing_connected_area():
    """
    Test case where a connected area_id does not exist in the map.
    Expected to log a warning and set the direction to None.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(
        return_value={
            "2": {
                "type": "area",
                "place_template": "Wonderwhirl Vale",
                "region": "1",
                "north": "99",  # Non-existent area
            }
        }
    )
    with patch("src.maps.map_manager.logger") as mock_logger:
        result = map_manager.get_cardinal_connections("2")
        mock_logger.warning.assert_called_with("Connected area '99' not found in map.")
    expected_result = {"north": None, "south": None, "east": None, "west": None}
    assert result == expected_result


def test_get_cardinal_connections_with_connected_area_missing_place_template():
    """
    Test case where the connected area exists but has no 'place_template'.
    Expected to log a warning and set 'place_template' to None.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(
        return_value={
            "2": {
                "type": "area",
                "place_template": "Wonderwhirl Vale",
                "region": "1",
                "north": "4",
            },
            "4": {
                "type": "area",
                # 'place_template' is missing
                "region": "1",
            },
        }
    )
    with patch("src.maps.map_manager.logger") as mock_logger:
        result = map_manager.get_cardinal_connections("2")
        mock_logger.warning.assert_called_with(
            "Place template not found for connected area '4'."
        )
    expected_result = {
        "north": {"identifier": "4", "place_template": None},
        "south": None,
        "east": None,
        "west": None,
    }
    assert result == expected_result


def test_get_cardinal_connections_with_all_directions():
    """
    Test case where the area has connections in all cardinal directions.
    Expected to return all connected areas with their identifiers and place_templates.
    """
    map_manager = MapManager(playthrough_name="test_playthrough")
    map_manager._load_map_file = MagicMock(
        return_value={
            "2": {
                "type": "area",
                "place_template": "Central Area",
                "region": "1",
                "north": "3",
                "south": "4",
                "east": "5",
                "west": "6",
            },
            "3": {"type": "area", "place_template": "Northern Area", "region": "1"},
            "4": {"type": "area", "place_template": "Southern Area", "region": "1"},
            "5": {"type": "area", "place_template": "Eastern Area", "region": "1"},
            "6": {"type": "area", "place_template": "Western Area", "region": "1"},
        }
    )
    expected_result = {
        "north": {"identifier": "3", "place_template": "Northern Area"},
        "south": {"identifier": "4", "place_template": "Southern Area"},
        "east": {"identifier": "5", "place_template": "Eastern Area"},
        "west": {"identifier": "6", "place_template": "Western Area"},
    }
    result = map_manager.get_cardinal_connections("2")
    assert result == expected_result
