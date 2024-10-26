from unittest.mock import MagicMock, patch

import pytest

from src.maps.weathers_manager import WeathersManager


@patch("src.maps.weathers_manager.read_json_file")
def test_get_all_weather_identifiers_returns_correct_identifiers(mock_read_json_file):
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "rainy": {"description": "Lots of rain and clouds"},
    }
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    weather_identifiers = weathers_manager.get_all_weather_identifiers()
    assert len(weather_identifiers) == 2
    assert "sunny" in weather_identifiers
    assert "rainy" in weather_identifiers


@patch("src.maps.weathers_manager.read_json_file")
def test_get_all_weather_identifiers_with_empty_weathers_file(mock_read_json_file):
    mock_filesystem_manager = MagicMock()
    weather_data = {}
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    weather_identifiers = weathers_manager.get_all_weather_identifiers()
    assert weather_identifiers == []


def test_get_current_weather_identifier_returns_correct_identifier():
    mock_map_manager = MagicMock()
    area_data = {"weather_identifier": "sunny"}
    mock_map_manager.get_current_area.return_value = area_data
    mock_map_manager_factory = MagicMock()
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager
    weathers_manager = WeathersManager(map_manager_factory=mock_map_manager_factory)
    result = weathers_manager.get_current_weather_identifier()
    expected = "sunny"
    assert result == expected


def test_get_current_weather_identifier_raises_key_error_when_missing():
    mock_map_manager = MagicMock()
    area_data = {"some_other_key": "value"}
    mock_map_manager.get_current_area.return_value = area_data
    mock_map_manager_factory = MagicMock()
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager
    weathers_manager = WeathersManager(map_manager_factory=mock_map_manager_factory)
    with pytest.raises(KeyError) as excinfo:
        weathers_manager.get_current_weather_identifier()
    assert "There's no key 'weather_identifier' in area data" in str(excinfo)


@patch("src.maps.weathers_manager.read_json_file")
def test_get_weather_description_returns_correct_description(mock_read_json_file):
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "rainy": {"description": "Lots of rain and clouds"},
    }
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    weather_identifier = "sunny"
    description = weathers_manager.get_weather_description(weather_identifier)
    expected_description = "Clear sky with bright sun"
    assert description == expected_description


@patch("src.maps.weathers_manager.read_json_file")
def test_get_weather_description_raises_key_error_when_identifier_missing(
    mock_read_json_file,
):
    mock_filesystem_manager = MagicMock()
    weather_data = {"sunny": {"description": "Clear sky with bright sun"}}
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    weather_identifier = "rainy"
    with pytest.raises(KeyError):
        weathers_manager.get_weather_description(weather_identifier)


@patch("src.maps.weathers_manager.read_json_file")
def test_get_weather_description_raises_key_error_when_description_missing(
    mock_read_json_file,
):
    mock_filesystem_manager = MagicMock()
    weather_data = {"sunny": {"not_description": "Should have description key"}}
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    weather_identifier = "sunny"
    with pytest.raises(KeyError):
        weathers_manager.get_weather_description(weather_identifier)


@patch("src.maps.weathers_manager.read_json_file")
def test_get_all_weather_identifiers_with_invalid_keys(mock_read_json_file):
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "": {"description": "No weather"},
    }
    mock_read_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()
    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )
    with pytest.raises(ValueError):
        weathers_manager.get_all_weather_identifiers()
