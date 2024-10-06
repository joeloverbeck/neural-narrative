import logging.config
import os
from typing import List

from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class PlaythroughManager:
    def __init__(
        self, playthrough_name: str, filesystem_manager: FilesystemManager = None
    ):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _update_playthrough_metadata_identifier(self, key: str, new_value: str):
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        playthrough_metadata[key] = new_value

        # Save the file back
        self._filesystem_manager.save_json_file(
            playthrough_metadata,
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            ),
        )

    def has_ongoing_dialogue(self, playthrough_name):
        return os.path.exists(
            self._filesystem_manager.get_file_path_to_ongoing_dialogue(playthrough_name)
        )

    def update_player_identifier(self, new_player_identifier):
        self._update_playthrough_metadata_identifier(
            "player_identifier", new_player_identifier
        )

    def get_player_identifier(self) -> str:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        return playthrough_metadata["player_identifier"]

    def get_world_template(self) -> str:
        playthrough_metadata_file = (
            self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                )
            )
        )

        return playthrough_metadata_file["world_template"]

    def get_hour(self) -> int:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        return playthrough_metadata["time"]["hour"]

    def update_hour(self, hour: int):
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        playthrough_metadata["time"]["hour"] = hour

        self._filesystem_manager.save_json_file(
            playthrough_metadata,
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            ),
        )

    def get_followers(self) -> List[str]:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        return playthrough_metadata["followers"]

    def add_follower(self, character_identifier):
        # First add the character to the list of followers of playthrough_metadata
        playthrough_metadata: dict = (
            self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                )
            )
        )

        playthrough_metadata["followers"].append(character_identifier)

        self._filesystem_manager.save_json_file(
            playthrough_metadata,
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            ),
        )

    def remove_follower(self, character_identifier):
        playthrough_metadata: dict = (
            self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                )
            )
        )

        playthrough_metadata["followers"] = [
            follower
            for follower in playthrough_metadata["followers"]
            if follower != character_identifier
        ]

        self._filesystem_manager.save_json_file(
            playthrough_metadata,
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            ),
        )

    def get_current_place_identifier(self) -> str:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
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
        file_path = self._filesystem_manager.get_file_path_to_adventure(
            self._playthrough_name
        )

        self._filesystem_manager.append_to_file(file_path, entry + "\n")
