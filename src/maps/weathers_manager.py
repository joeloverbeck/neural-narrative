from typing import Optional, List, Dict

from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager
from src.maps.factories.map_manager_factory import MapManagerFactory


class WeathersManager:

    def __init__(
        self,
        map_manager_factory: MapManagerFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._map_manager_factory = map_manager_factory

        self._path_manager = path_manager or PathManager()

    def _load_weathers_file(self) -> Dict[str, Dict[str, str]]:
        return read_json_file(self._path_manager.get_weathers_path())

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
