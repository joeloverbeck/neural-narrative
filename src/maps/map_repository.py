from typing import Optional, Dict
from src.filesystem.filesystem_manager import FilesystemManager


class MapRepository:

    def __init__(self, playthrough_name: str, filesystem_manager: Optional[
        FilesystemManager] = None):
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def load_map_data(self) -> Dict:
        return self._filesystem_manager.load_existing_or_new_json_file(self
                                                                       ._filesystem_manager.get_file_path_to_map(
            self._playthrough_name))

    def save_map_data(self, map_data: Dict):
        self._filesystem_manager.save_json_file(map_data, self.
                                                _filesystem_manager.get_file_path_to_map(self._playthrough_name))
