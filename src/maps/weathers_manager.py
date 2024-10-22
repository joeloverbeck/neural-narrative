from typing import Optional, List, Dict

from src.base.constants import WEATHERS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.map_manager_factory import MapManagerFactory


class WeathersManager:

    def __init__(
        self,
        map_manager_factory: MapManagerFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._map_manager_factory = map_manager_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _load_weathers_file(self) -> Dict[str, Dict[str, str]]:
        return self._filesystem_manager.load_existing_or_new_json_file(WEATHERS_FILE)

    def get_all_weather_identifiers(self) -> [List[str]]:
        weather_identifiers = []

        for key, value in self._load_weathers_file().items():
            if not key:
                raise ValueError(
                    f"Found an empty key. Items: {self._load_weathers_file().items()}"
                )
            weather_identifiers.append(key)

        return weather_identifiers

    def get_current_weather_identifier(self) -> str:
        area_data = self._map_manager_factory.create_map_manager().get_current_area()
        if not "weather_identifier" in area_data:
            raise KeyError(
                f"There's no key 'weather_identifier' in area data: {area_data}"
            )
        return area_data["weather_identifier"]

    def get_weather_description(self, weather_identifier: str) -> str:
        return self._load_weathers_file()[weather_identifier]["description"]
