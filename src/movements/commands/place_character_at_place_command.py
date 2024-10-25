import logging
from typing import Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.filesystem.filesystem_manager import FilesystemManager
from src.movements.exceptions import PlaceCharacterAtPlaceError

logger = logging.getLogger(__name__)


class PlaceCharacterAtPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        place_identifier: str,
        playthrough_manager: Optional[PlaythroughManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(place_identifier, "place_identifier")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._place_identifier = place_identifier

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        # First ensure that the character doesn't exist in the list of followers.
        if self._character_identifier in self._playthrough_manager.get_followers():
            raise PlaceCharacterAtPlaceError(
                f"Character {self._character_identifier} is one of the followers. "
                "If you intended to remove them from the followers and place them at a location, you should remove them from the followers first."
            )

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )

        place = map_file.get(self._place_identifier)

        if not place:
            raise ValueError(f"Place ID {self._place_identifier} not found.")

        place_type = place.get("type")

        if place_type not in ("area", "location"):
            raise PlaceCharacterAtPlaceError(
                f"Place type '{place_type}' cannot house characters."
            )

        characters_list = place.get("characters")

        if characters_list is None:
            characters_list = []
            place["characters"] = characters_list
        if self._character_identifier in characters_list:
            raise PlaceCharacterAtPlaceError(
                f"Character {self._character_identifier} is already at place {self._place_identifier}."
            )

        characters_list.append(self._character_identifier)

        # Save new list of characters.
        self._filesystem_manager.save_json_file(
            map_file,
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name),
        )

        logger.info(
            f"Character '{self._character_identifier}' placed at {place_type} '{self._place_identifier}'. Current character list: {characters_list}"
        )
