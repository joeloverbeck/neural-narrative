from typing import Optional, List, Dict

from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager


class WeathersManager:

    def __init__(
        self,
        path_manager: Optional[PathManager] = None,
    ):
        self._path_manager = path_manager or PathManager()

    def _load_weathers_file(self) -> Dict[str, Dict[str, str]]:
        return read_json_file(self._path_manager.get_weathers_path())

    def get_all_weather_identifiers(self) -> List[str]:
        weather_identifiers = []

        for key, value in self._load_weathers_file().items():
            if not key:
                raise ValueError(
                    f"Found an empty key. Items: {self._load_weathers_file().items()}"
                )
            weather_identifiers.append(key)

        return weather_identifiers

    def get_weather_description(self, weather_identifier: str) -> str:
        return self._load_weathers_file()[weather_identifier]["description"]
