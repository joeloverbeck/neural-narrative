import logging.config

from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager

logger = logging.getLogger(__name__)


class PlaythroughManager:
    def __init__(self, playthrough_name: str, filesystem_manager: FilesystemManager = None,
                 map_manager: MapManager = None):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._map_manager = map_manager or MapManager(playthrough_name)

    def _update_playthrough_metadata_identifier(self, key: str, new_value: str):
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        playthrough_metadata[key] = new_value

        # Save the file back
        self._filesystem_manager.save_json_file(playthrough_metadata,
                                                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                                                    self._playthrough_name))

    def place_character_at_current_place(self, player_identifier: str):
        if not player_identifier:
            raise ValueError("player_identifier must not be empty.")

        current_place = self.get_current_place()

        # Must now include the character identifier at current place
        self._map_manager.place_character_at_place(player_identifier, current_place)

    def update_player_identifier(self, new_player_identifier):
        self._update_playthrough_metadata_identifier("player_identifier", new_player_identifier)

    def get_player_identifier(self) -> str:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        return playthrough_metadata["player_identifier"]

    def get_current_place(self) -> str:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        return playthrough_metadata["current_place"]

    def update_current_place(self, new_current_place_identifier: str):
        self._update_playthrough_metadata_identifier("current_place", new_current_place_identifier)

        logger.info(f"Updated playthrough current place to '{new_current_place_identifier}'.")
