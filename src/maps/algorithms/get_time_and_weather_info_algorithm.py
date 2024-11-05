from typing import Optional

from src.base.constants import WEATHER_ICON_MAPPING
from src.base.validators import validate_non_empty_string
from src.filesystem.config_loader import ConfigLoader
from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.dataclasses.get_time_and_weather_info_algorithm_data import (
    GetTimeAndWeatherInfoAlgorithmData,
)
from src.maps.weathers_manager import WeathersManager
from src.time.time_manager import TimeManager


class GetTimeAndWeatherInfoAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        get_current_weather_identifier_algorithm: GetCurrentWeatherIdentifierAlgorithm,
        time_manager: Optional[TimeManager] = None,
        weathers_manager: Optional[WeathersManager] = None,
        config_loader: Optional[ConfigLoader] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._get_current_weather_identifier_algorithm = (
            get_current_weather_identifier_algorithm
        )

        self._time_manager = time_manager or TimeManager(playthrough_name)
        self._weathers_manager = weathers_manager or WeathersManager()
        self._config_loader = config_loader or ConfigLoader()

    def do_algorithm(self) -> GetTimeAndWeatherInfoAlgorithmData:
        current_hour = self._time_manager.get_hour()
        current_time_of_day = self._time_manager.get_time_of_the_day()

        current_weather = self._get_current_weather_identifier_algorithm.do_algorithm()

        current_weather_description = self._weathers_manager.get_weather_description(
            current_weather
        )

        weather_icon_class = WEATHER_ICON_MAPPING.get(
            current_weather, self._config_loader.get_default_weather_icon()
        )

        all_weathers = self._weathers_manager.get_all_weather_identifiers()

        return GetTimeAndWeatherInfoAlgorithmData(
            current_hour,
            current_time_of_day,
            current_weather,
            current_weather_description,
            weather_icon_class,
            all_weathers,
        )
