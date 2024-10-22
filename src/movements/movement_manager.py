import logging

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_manager_factory import PlaceManagerFactory

logger = logging.getLogger(__name__)


class MovementManager:

    def __init__(
        self,
            playthrough_name: str,
            place_manager_factory: PlaceManagerFactory,
        playthrough_manager: PlaythroughManager = None,
        filesystem_manager: FilesystemManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._place_manager_factory = place_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def place_character_at_current_place(self, player_identifier: str):
        current_place = self._playthrough_manager.get_current_place_identifier()
        self.place_character_at_place(player_identifier, current_place)

    def place_character_at_place(
            self, character_identifier: str, place_identifier: str
    ):
        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID {place_identifier} not found.")
        place_type = place.get("type")
        if place_type not in ("area", "location"):
            raise ValueError(f"Place type '{place_type}' cannot house characters.")
        characters_list = place.get("characters")
        if characters_list is None:
            characters_list = []
            place["characters"] = characters_list
        if character_identifier in characters_list:
            raise ValueError(
                f"Character {character_identifier} is already at place {place_identifier}."
            )
        characters_list.append(character_identifier)
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
        self._playthrough_manager.add_follower(character_identifier)
        self._place_manager_factory.create_place_manager().remove_character_from_place(
            character_identifier, current_place_identifier
        )

    def remove_follower(
            self, character_identifier: str, current_place_identifier: str
    ) -> None:
        self._playthrough_manager.remove_follower(character_identifier)
        self.place_character_at_place(character_identifier, current_place_identifier)
