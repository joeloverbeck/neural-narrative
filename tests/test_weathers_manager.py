# test_weathers_manager.py

from unittest.mock import MagicMock

import pytest

from src.base.required_string import RequiredString
from src.maps.weathers_manager import WeathersManager


def test_get_all_weather_identifiers_returns_correct_identifiers():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "rainy": {"description": "Lots of rain and clouds"},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    weather_identifiers = weathers_manager.get_all_weather_identifiers()

    # Assert
    assert len(weather_identifiers) == 2
    assert RequiredString("sunny") in weather_identifiers
    assert RequiredString("rainy") in weather_identifiers


def test_get_all_weather_identifiers_with_empty_weathers_file():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {}  # Empty dictionary
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act
    weather_identifiers = weathers_manager.get_all_weather_identifiers()

    # Assert
    assert weather_identifiers == []


def test_get_current_weather_identifier_returns_correct_identifier():
    # Arrange
    mock_map_manager = MagicMock()
    area_data = {"weather_identifier": "sunny"}
    mock_map_manager.get_current_area.return_value = area_data
    mock_map_manager_factory = MagicMock()
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    weathers_manager = WeathersManager(map_manager_factory=mock_map_manager_factory)

    # Act
    result = weathers_manager.get_current_weather_identifier()

    # Assert
    expected = RequiredString("sunny")
    assert result == expected


def test_get_current_weather_identifier_raises_key_error_when_missing():
    # Arrange
    mock_map_manager = MagicMock()
    area_data = {"some_other_key": "value"}
    mock_map_manager.get_current_area.return_value = area_data
    mock_map_manager_factory = MagicMock()
    mock_map_manager_factory.create_map_manager.return_value = mock_map_manager

    weathers_manager = WeathersManager(map_manager_factory=mock_map_manager_factory)

    # Act and Assert
    with pytest.raises(KeyError) as excinfo:
        weathers_manager.get_current_weather_identifier()

    assert "There's no key 'weather_identifier' in area data" in str(excinfo.value)


def test_get_weather_description_returns_correct_description():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "rainy": {"description": "Lots of rain and clouds"},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    weather_identifier = RequiredString("sunny")

    # Act
    description = weathers_manager.get_weather_description(weather_identifier)

    # Assert
    expected_description = RequiredString("Clear sky with bright sun")
    assert description == expected_description


def test_get_weather_description_raises_key_error_when_identifier_missing():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    weather_identifier = RequiredString("rainy")

    # Act and Assert
    with pytest.raises(KeyError):
        weathers_manager.get_weather_description(weather_identifier)


def test_get_weather_description_raises_key_error_when_description_missing():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"not_description": "Should have description key"},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    weather_identifier = RequiredString("sunny")

    # Act and Assert
    with pytest.raises(KeyError):
        weathers_manager.get_weather_description(weather_identifier)


def test_get_all_weather_identifiers_with_invalid_keys():
    # Arrange
    mock_filesystem_manager = MagicMock()
    weather_data = {
        "sunny": {"description": "Clear sky with bright sun"},
        "": {"description": "No weather"},
    }
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = weather_data
    mock_map_manager_factory = MagicMock()

    weathers_manager = WeathersManager(
        map_manager_factory=mock_map_manager_factory,
        filesystem_manager=mock_filesystem_manager,
    )

    # Act and Assert
    with pytest.raises(ValueError):
        weathers_manager.get_all_weather_identifiers()
