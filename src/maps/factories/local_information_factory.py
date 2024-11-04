from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.weathers_manager import WeathersManager
from src.time.time_manager import TimeManager


class LocalInformationFactory:

    def __init__(
        self,
        playthrough_name: str,
        get_current_weather_identifier_algorithm: GetCurrentWeatherIdentifierAlgorithm,
        place_description_manager: PlaceDescriptionManager,
        weathers_manager: WeathersManager,
        time_manager: Optional[TimeManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._get_current_weather_identifier_algorithm = (
            get_current_weather_identifier_algorithm
        )
        self._place_description_manager = place_description_manager
        self._weathers_manager = weathers_manager

        self._time_manager = time_manager or TimeManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

    def get_information(self) -> str:
        setting_description = self._place_description_manager.get_place_description(
            self._playthrough_manager.get_current_place_identifier()
        )

        local_information = read_file(self._path_manager.get_local_information_path())

        party_data_for_prompt = {
            "setting_description": setting_description,
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "weather": self._weathers_manager.get_weather_description(
                self._get_current_weather_identifier_algorithm.do_algorithm()
            ),
        }

        return local_information.format(**party_data_for_prompt)
