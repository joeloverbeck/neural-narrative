import logging.config
import os
from typing import List, Optional

from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class PlaythroughManager:
    def __init__(
        self,
        playthrough_name: RequiredString,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _update_playthrough_metadata_identifier(
        self, key: RequiredString, new_value: RequiredString
    ):
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        playthrough_metadata[key.value] = new_value.value

        # Save the file back
        self._filesystem_manager.save_json_file(
            playthrough_metadata,
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            ),
        )

    def has_ongoing_dialogue(self, playthrough_name):
        return os.path.exists(
            self._filesystem_manager.get_file_path_to_ongoing_dialogue(
                playthrough_name
            ).value
        )

    def update_player_identifier(self, new_player_identifier: RequiredString):
        self._update_playthrough_metadata_identifier(
            RequiredString("player_identifier"), new_player_identifier
        )

    def get_player_identifier(self) -> RequiredString:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        return RequiredString(playthrough_metadata["player_identifier"])

    def get_story_universe_template(self) -> RequiredString:
        playthrough_metadata_file = (
            self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                )
            )
        )

        return RequiredString(playthrough_metadata_file["story_universe_template"])

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

    def get_followers(self) -> List[RequiredString]:
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )

        return [
            RequiredString(follower) for follower in playthrough_metadata["followers"]
        ]

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

    def update_current_place(self, new_current_place_identifier: RequiredString):
        self._update_playthrough_metadata_identifier(
            RequiredString("current_place"), new_current_place_identifier
        )

        logger.info(
            f"Updated playthrough current place to '{new_current_place_identifier}'."
        )

    def add_to_adventure(self, entry: RequiredString):
        file_path = self._filesystem_manager.get_file_path_to_adventure(
            self._playthrough_name
        )

        self._filesystem_manager.append_to_file(
            file_path, RequiredString(entry.value + "\n")
        )
