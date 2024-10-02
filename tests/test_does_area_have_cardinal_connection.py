# Sample map data without cardinal connections
from typing import cast

import pytest

from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.enums import CardinalDirection
from src.maps.map_manager import MapManager

map_data = {
    "1": {"type": "region", "place_template": "Gigantis"},
    "2": {
        "type": "area",
        "place_template": "Ironspire Peaks",
        "region": "1",
        "locations": [],
        "characters": ["4"],
        "visited": True,
    },
    "3": {
        "type": "location",
        "place_template": "The Forge of Fallen Heroes",
        "area": "2",
        "characters": ["1", "2"],
        "visited": True,
    },
}

# Sample map data with a cardinal connection
map_data_with_connection = {
    "1": {"type": "region", "place_template": "Gigantis"},
    "2": {
        "type": "area",
        "place_template": "Ironspire Peaks",
        "region": "1",
        "locations": [],
        "characters": ["4"],
        "visited": True,
        "north": "5",  # Adding a north connection to area '5'
    },
    "3": {
        "type": "location",
        "place_template": "The Forge of Fallen Heroes",
        "area": "2",
        "characters": ["1", "2"],
        "visited": True,
    },
    "5": {
        "type": "area",
        "place_template": "Crystal Caverns",
        "region": "1",
        "locations": [],
        "characters": [],
        "visited": False,
    },
}


# Mocked dependencies
class FilesystemManagerMock:
    def __init__(self, map_data_for_fs: dict):
        self._map_data = map_data_for_fs

    def load_existing_or_new_json_file(self, file_path):
        return self._map_data

    @staticmethod
    def get_file_path_to_map(playthrough_name):
        return f"{playthrough_name}_map.json"


class IdentifiersManagerMock:
    pass


class PlaythroughManagerMock:
    pass


# MapManager class definition (assuming it's imported or defined in the test file)
# ...


# Test when area_identifier is empty
def test_does_area_have_cardinal_connection_with_empty_area_identifier():
    mock_fs_manager = FilesystemManagerMock(map_data)
    map_manager = MapManager(
        playthrough_name="test_playthrough",
        filesystem_manager=cast(FilesystemManager, mock_fs_manager),
    )

    with pytest.raises(ValueError) as exc_info:
        map_manager.does_area_have_cardinal_connection("", CardinalDirection.NORTH)
    assert "area_identifier can't be empty." in str(exc_info.value)


# Test when area_identifier does not exist
def test_does_area_have_cardinal_connection_with_non_existent_area_identifier():
    mock_fs_manager = FilesystemManagerMock(map_data)
    map_manager = MapManager(
        playthrough_name="test_playthrough",
        filesystem_manager=cast(FilesystemManager, mock_fs_manager),
    )

    with pytest.raises(KeyError) as exc_info:
        map_manager.does_area_have_cardinal_connection("99", CardinalDirection.NORTH)
    assert "99" in str(exc_info.value)


# Test when area_identifier exists but is not of type 'area'
def test_does_area_have_cardinal_connection_with_non_area_type_identifier():
    mock_fs_manager = FilesystemManagerMock(map_data)
    map_manager = MapManager(
        playthrough_name="test_playthrough",
        filesystem_manager=cast(FilesystemManager, mock_fs_manager),
    )

    # Identifier '1' is a 'region'
    with pytest.raises(ValueError) as exc_info:
        map_manager.does_area_have_cardinal_connection("1", CardinalDirection.NORTH)
    assert "didn't belong to an area, but to a 'region'" in str(exc_info.value)

    # Identifier '3' is a 'location'
    with pytest.raises(ValueError) as exc_info:
        map_manager.does_area_have_cardinal_connection("3", CardinalDirection.NORTH)
    assert "didn't belong to an area, but to a 'location'" in str(exc_info.value)


# Test when area has the cardinal connection
def test_does_area_have_cardinal_connection_with_existing_connection():
    mock_fs_manager = FilesystemManagerMock(map_data_with_connection)
    map_manager = MapManager(
        playthrough_name="test_playthrough",
        filesystem_manager=cast(FilesystemManager, mock_fs_manager),
    )

    result = map_manager.does_area_have_cardinal_connection(
        "2", CardinalDirection.NORTH
    )
    assert result is True


# Test when area does not have the cardinal connection
def test_does_area_have_cardinal_connection_with_no_connection():
    mock_fs_manager = FilesystemManagerMock(map_data)
    map_manager = MapManager(
        playthrough_name="test_playthrough",
        filesystem_manager=cast(FilesystemManager, mock_fs_manager),
    )

    result = map_manager.does_area_have_cardinal_connection(
        "2", CardinalDirection.SOUTH
    )
    assert result is False
