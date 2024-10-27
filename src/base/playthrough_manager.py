import logging.config
import os
from pathlib import Path
from typing import List, Optional

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    append_to_file,
    read_json_file,
    write_json_file,
    remove_folder,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class PlaythroughManager:

    def __init__(
        self,
        playthrough_name: str,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._path_manager = path_manager or PathManager()

    def _update_playthrough_metadata_identifier(self, key: str, new_value: str):
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )

        playthrough_metadata[key] = new_value

        write_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name),
            playthrough_metadata,
        )

    def has_ongoing_dialogue(self, playthrough_name):
        return os.path.exists(
            self._path_manager.get_ongoing_dialogue_path(playthrough_name)
        )

    def update_player_identifier(self, new_player_identifier: str):
        self._update_playthrough_metadata_identifier(
            "player_identifier", new_player_identifier
        )

    def get_player_identifier(self) -> str:
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        return playthrough_metadata["player_identifier"]

    def get_story_universe_template(self) -> str:
        playthrough_metadata_file = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        logger.warning(playthrough_metadata_file)
        return playthrough_metadata_file["story_universe_template"]

    def get_hour(self) -> int:
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        return playthrough_metadata["time"]["hour"]

    def update_hour(self, hour: int):
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        playthrough_metadata["time"]["hour"] = hour

        write_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name),
            playthrough_metadata,
        )

    def get_followers(self) -> List[str]:
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        return [follower for follower in playthrough_metadata["followers"]]

    def add_follower(self, character_identifier):
        playthrough_metadata: dict = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        playthrough_metadata["followers"].append(character_identifier)

        write_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name),
            playthrough_metadata,
        )

    def remove_follower(self, character_identifier):
        playthrough_metadata: dict = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )

        playthrough_metadata["followers"] = [
            follower
            for follower in playthrough_metadata["followers"]
            if follower != character_identifier
        ]

        write_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name),
            playthrough_metadata,
        )

    def get_current_place_identifier(self) -> str:
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        return playthrough_metadata["current_place"]

    def update_current_place(self, new_current_place_identifier: str):
        self._update_playthrough_metadata_identifier(
            "current_place", new_current_place_identifier
        )
        logger.info(
            f"Updated playthrough current place to '{new_current_place_identifier}'."
        )

    def add_to_adventure(self, entry: str):
        file_path = self._path_manager.get_adventure_path(self._playthrough_name)
        append_to_file(Path(file_path), entry + "\n")

    def delete_playthrough_folder(self, playthrough_name: str) -> None:
        """
        Delete the playthrough folder for the given playthrough name.

        Args:
            playthrough_name (str): The name of the playthrough whose folder is to be deleted.
        """
        folder_path = self._path_manager.get_playthrough_path(playthrough_name)

        remove_folder(folder_path)
