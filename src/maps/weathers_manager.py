from typing import Optional, List, Dict

from src.constants import WEATHERS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.maps.weather_identifier import WeatherIdentifier
from src.playthrough_manager import PlaythroughManager
from src.playthrough_name import PlaythroughName


class WeathersManager:

    def __init__(
        self,
        playthrough_name: PlaythroughName,
        map_manager: Optional[MapManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._map_manager = map_manager or MapManager(playthrough_name.value)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name.value
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _load_weathers_file(self) -> Dict[str, Dict[str, str]]:
        return self._filesystem_manager.load_existing_or_new_json_file(WEATHERS_FILE)

    def get_all_weather_identifiers(self) -> [List[str]]:
        return [key for key, value in self._load_weathers_file().items()]

    def get_current_weather_identifier(self) -> WeatherIdentifier:
        area_data = self._map_manager.get_current_area()

        if not "weather_identifier" in area_data:
            raise KeyError(
                f"There's no key 'weather_identifier' in area data: {area_data}"
            )

        return WeatherIdentifier(area_data["weather_identifier"])

    def get_weather_description(self, weather_identifier: WeatherIdentifier) -> str:
        if not isinstance(weather_identifier, WeatherIdentifier):
            raise TypeError(
                "Expected weather_identifier to be of type WeatherIdentifier."
            )

        return self._load_weathers_file()[weather_identifier.value]["description"]
