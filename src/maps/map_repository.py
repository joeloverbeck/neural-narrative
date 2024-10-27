from typing import Optional, Dict

from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager


class MapRepository:

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

    def load_map_data(self) -> Dict:
        return read_json_file(self._path_manager.get_map_path(self._playthrough_name))

    def save_map_data(self, map_data: Dict):
        write_json_file(
            self._path_manager.get_map_path(self._playthrough_name),
            map_data,
        )
