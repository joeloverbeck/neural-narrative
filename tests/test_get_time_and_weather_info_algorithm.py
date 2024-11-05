from unittest.mock import MagicMock, patch

import pytest

from src.base.constants import WEATHER_ICON_MAPPING
from src.filesystem.config_loader import ConfigLoader
from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.algorithms.get_time_and_weather_info_algorithm import (
    GetTimeAndWeatherInfoAlgorithm,
)
from src.maps.weathers_manager import WeathersManager
from src.time.time_manager import TimeManager


def test_do_algorithm_with_valid_inputs():
    # Mocks
    playthrough_name = "test_playthrough"
    mock_time_manager = MagicMock(spec=TimeManager)
    mock_time_manager.get_hour.return_value = 14
    mock_time_manager.get_time_of_the_day.return_value = "afternoon"

    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )
    mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = "sunny"

    mock_weathers_manager = MagicMock(spec=WeathersManager)
    mock_weathers_manager.get_weather_description.return_value = "A bright sunny day"
    mock_weathers_manager.get_all_weather_identifiers.return_value = [
        "sunny",
        "rainy",
        "cloudy",
    ]

    mock_config_loader = MagicMock(spec=ConfigLoader)

    # Instantiate the class
    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
        weathers_manager=mock_weathers_manager,
        config_loader=mock_config_loader,
    )

    # Call do_algorithm
    result = algorithm.do_algorithm()

    # Assertions
    assert result.current_hour == 14
    assert result.current_time_of_day == "afternoon"
    assert result.current_weather == "sunny"
    assert result.current_weather_description == "A bright sunny day"
    assert result.weather_icon_class == WEATHER_ICON_MAPPING["sunny"]
    assert result.all_weathers == ["sunny", "rainy", "cloudy"]


def test_do_algorithm_with_unknown_weather():
    # Mocks
    playthrough_name = "test_playthrough"
    mock_time_manager = MagicMock(spec=TimeManager)
    mock_time_manager.get_hour.return_value = 10
    mock_time_manager.get_time_of_the_day.return_value = "morning"

    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )
    mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = (
        "unknown_weather"
    )

    mock_weathers_manager = MagicMock(spec=WeathersManager)
    mock_weathers_manager.get_weather_description.return_value = "Unknown weather"
    mock_weathers_manager.get_all_weather_identifiers.return_value = [
        "sunny",
        "rainy",
        "cloudy",
    ]

    mock_config_loader = MagicMock(spec=ConfigLoader)
    mock_config_loader.get_default_weather_icon.return_value = "fas fa-question"

    # Instantiate the class
    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
        weathers_manager=mock_weathers_manager,
        config_loader=mock_config_loader,
    )

    # Call do_algorithm
    result = algorithm.do_algorithm()

    # Assertions
    assert result.current_hour == 10
    assert result.current_time_of_day == "morning"
    assert result.current_weather == "unknown_weather"
    assert result.current_weather_description == "Unknown weather"
    assert result.weather_icon_class == "fas fa-question"  # default icon
    assert result.all_weathers == ["sunny", "rainy", "cloudy"]


def test_init_with_empty_playthrough_name():
    playthrough_name = ""
    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )

    with pytest.raises(ValueError):
        algorithm = GetTimeAndWeatherInfoAlgorithm(
            playthrough_name=playthrough_name,
            get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        )


def test_init_with_provided_time_manager():
    playthrough_name = "test_playthrough"
    mock_time_manager = MagicMock(spec=TimeManager)
    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )

    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
    )

    assert algorithm._time_manager is mock_time_manager


def test_init_without_provided_time_manager():
    playthrough_name = "test_playthrough"
    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )

    with patch(
        "src.maps.algorithms.get_time_and_weather_info_algorithm.TimeManager"
    ) as MockTimeManager:
        algorithm = GetTimeAndWeatherInfoAlgorithm(
            playthrough_name=playthrough_name,
            get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        )

        MockTimeManager.assert_called_once_with(playthrough_name)
        assert algorithm._time_manager == MockTimeManager.return_value


def test_do_algorithm_with_different_times_of_day():
    # Mocks
    playthrough_name = "test_playthrough"
    times_of_day = ["morning", "afternoon", "evening", "night"]

    for time_of_day in times_of_day:
        mock_time_manager = MagicMock(spec=TimeManager)
        mock_time_manager.get_hour.return_value = 12  # arbitrary hour
        mock_time_manager.get_time_of_the_day.return_value = time_of_day

        mock_get_current_weather_identifier_algorithm = MagicMock(
            spec=GetCurrentWeatherIdentifierAlgorithm
        )
        mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = (
            "sunny"
        )

        mock_weathers_manager = MagicMock(spec=WeathersManager)
        mock_weathers_manager.get_weather_description.return_value = (
            "A bright sunny day"
        )
        mock_weathers_manager.get_all_weather_identifiers.return_value = [
            "sunny",
            "rainy",
            "cloudy",
        ]

        mock_config_loader = MagicMock(spec=ConfigLoader)

        # Instantiate the class
        algorithm = GetTimeAndWeatherInfoAlgorithm(
            playthrough_name=playthrough_name,
            get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
            time_manager=mock_time_manager,
            weathers_manager=mock_weathers_manager,
            config_loader=mock_config_loader,
        )

        # Call do_algorithm
        result = algorithm.do_algorithm()

        # Assertions
        assert result.current_time_of_day == time_of_day


def test_do_algorithm_with_different_weathers():
    # Mocks
    playthrough_name = "test_playthrough"
    weathers = ["sunny", "rainy", "snowy", "unknown_weather"]

    for weather in weathers:
        mock_time_manager = MagicMock(spec=TimeManager)
        mock_time_manager.get_hour.return_value = 12
        mock_time_manager.get_time_of_the_day.return_value = "afternoon"

        mock_get_current_weather_identifier_algorithm = MagicMock(
            spec=GetCurrentWeatherIdentifierAlgorithm
        )
        mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = (
            weather
        )

        mock_weathers_manager = MagicMock(spec=WeathersManager)
        mock_weathers_manager.get_weather_description.return_value = (
            f"{weather} description"
        )
        mock_weathers_manager.get_all_weather_identifiers.return_value = [
            "sunny",
            "rainy",
            "snowy",
        ]

        mock_config_loader = MagicMock(spec=ConfigLoader)
        mock_config_loader.get_default_weather_icon.return_value = "fas fa-question"

        # Instantiate the class
        algorithm = GetTimeAndWeatherInfoAlgorithm(
            playthrough_name=playthrough_name,
            get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
            time_manager=mock_time_manager,
            weathers_manager=mock_weathers_manager,
            config_loader=mock_config_loader,
        )

        # Call do_algorithm
        result = algorithm.do_algorithm()

        # Assertions
        assert result.current_weather == weather
        assert result.current_weather_description == f"{weather} description"

        expected_icon = WEATHER_ICON_MAPPING.get(weather, "fas fa-question")
        assert result.weather_icon_class == expected_icon


def test_do_algorithm_with_all_weathers():
    # Mocks
    playthrough_name = "test_playthrough"
    all_weathers = ["sunny", "rainy", "cloudy", "stormy"]

    mock_time_manager = MagicMock(spec=TimeManager)
    mock_time_manager.get_hour.return_value = 15
    mock_time_manager.get_time_of_the_day.return_value = "afternoon"

    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )
    mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = "rainy"

    mock_weathers_manager = MagicMock(spec=WeathersManager)
    mock_weathers_manager.get_weather_description.return_value = "A rainy day"
    mock_weathers_manager.get_all_weather_identifiers.return_value = all_weathers

    mock_config_loader = MagicMock(spec=ConfigLoader)

    # Instantiate the class
    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
        weathers_manager=mock_weathers_manager,
        config_loader=mock_config_loader,
    )

    # Call do_algorithm
    result = algorithm.do_algorithm()

    # Assertions
    assert result.all_weathers == all_weathers


def test_weather_icon_mapping_fallback():
    # Mocks
    playthrough_name = "test_playthrough"
    current_weather = "unknown_weather"

    mock_time_manager = MagicMock(spec=TimeManager)
    mock_time_manager.get_hour.return_value = 16
    mock_time_manager.get_time_of_the_day.return_value = "afternoon"

    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )
    mock_get_current_weather_identifier_algorithm.do_algorithm.return_value = (
        current_weather
    )

    mock_weathers_manager = MagicMock(spec=WeathersManager)
    mock_weathers_manager.get_weather_description.return_value = "Unknown weather"
    mock_weathers_manager.get_all_weather_identifiers.return_value = [
        "sunny",
        "rainy",
        "hail",
    ]

    mock_config_loader = MagicMock(spec=ConfigLoader)
    mock_config_loader.get_default_weather_icon.return_value = "fas fa-question"

    # Instantiate the class
    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
        weathers_manager=mock_weathers_manager,
        config_loader=mock_config_loader,
    )

    # Call do_algorithm
    result = algorithm.do_algorithm()

    # Assertions
    assert result.weather_icon_class == "fas fa-question"  # default icon


def test_exception_propagation():
    # Mocks
    playthrough_name = "test_playthrough"

    mock_time_manager = MagicMock(spec=TimeManager)
    mock_time_manager.get_hour.side_effect = Exception("Time manager error")

    mock_get_current_weather_identifier_algorithm = MagicMock(
        spec=GetCurrentWeatherIdentifierAlgorithm
    )
    mock_weathers_manager = MagicMock(spec=WeathersManager)
    mock_config_loader = MagicMock(spec=ConfigLoader)

    algorithm = GetTimeAndWeatherInfoAlgorithm(
        playthrough_name=playthrough_name,
        get_current_weather_identifier_algorithm=mock_get_current_weather_identifier_algorithm,
        time_manager=mock_time_manager,
        weathers_manager=mock_weathers_manager,
        config_loader=mock_config_loader,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()
    assert str(exc_info.value) == "Time manager error"
