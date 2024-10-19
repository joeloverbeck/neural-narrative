import logging

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager

logger = logging.getLogger(__name__)


class MovementManager:
    def __init__(
        self,
        playthrough_name: str,
        playthrough_manager: PlaythroughManager = None,
        filesystem_manager: FilesystemManager = None,
        map_manager: MapManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def place_character_at_current_place(self, player_identifier: str):
        if not player_identifier:
            raise ValueError("player_identifier must not be empty.")

        current_place = self._playthrough_manager.get_current_place_identifier()

        # Must now include the character identifier at current place
        self.place_character_at_place(player_identifier, current_place)

    def place_character_at_place(self, character_identifier, place_identifier):
        if not character_identifier:
            raise ValueError("character_identifier should not be empty.")
        if not place_identifier:
            raise ValueError("place_identifier should not be empty.")

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )

        # Get the place data
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID {place_identifier} not found.")

        # Ensure the place type is 'area' or 'location'
        place_type = place.get("type")
        if place_type not in ("area", "location"):
            raise ValueError(f"Place type '{place_type}' cannot house characters.")

        # Get the 'characters' list
        characters_list = place.get("characters")
        if characters_list is None:
            # Initialize the list if not present
            characters_list = []

            place["characters"] = characters_list

        # Check if character is already present
        if character_identifier in characters_list:
            raise ValueError(
                f"Character {character_identifier} is already at place {place_identifier}."
            )

        # Add the character identifier to the list
        characters_list.append(character_identifier)

        # Save the updated map file
        self._filesystem_manager.save_json_file(
            map_file,
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name),
        )

        logger.info(
            f"Character '{character_identifier}' placed at {place_type} '{place_identifier}'. Current character list: {characters_list}"
        )

    def add_follower(
        self, character_identifier: str, current_place_identifier: str
    ) -> None:
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")
        if not current_place_identifier:
            raise ValueError("current_place_identifier can't be empty.")

        # First add the character to the list of followers of playthrough_metadata
        self._playthrough_manager.add_follower(character_identifier)

        # Now we need to remove this character identifier from its current place.
        self._map_manager.remove_character_from_place(
            character_identifier, current_place_identifier
        )

    def remove_follower(self, character_identifier: str, current_place_identifier: str):
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")
        if not current_place_identifier:
            raise ValueError("current_place_identifier can't be empty.")

        # First we have to remove the character from the playthrough_metadata "followers" list
        self._playthrough_manager.remove_follower(character_identifier)

        # Now we need to add this character identifier to the current place.
        self.place_character_at_place(character_identifier, current_place_identifier)
