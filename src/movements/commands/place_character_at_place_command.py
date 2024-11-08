import logging
from typing import Optional, List

from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.map_repository import MapRepository
from src.movements.exceptions import PlaceCharacterAtPlaceError

logger = logging.getLogger(__name__)


class PlaceCharacterAtPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        place_identifier: str,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(place_identifier, "place_identifier")

        self._character_identifier = character_identifier
        self._place_identifier = place_identifier

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._map_repository = map_repository or MapRepository(playthrough_name)

    def _validate_character_is_not_follower(self):
        if self._character_identifier in self._playthrough_manager.get_followers():
            raise PlaceCharacterAtPlaceError(
                f"Character {self._character_identifier} is one of the followers. "
                "If you intended to remove them from the followers and place them at a location, you should remove them from the followers first."
            )

    @staticmethod
    def _validate_place_type_can_house_characters(place_type: str):
        if place_type not in (
            TemplateType.AREA.value,
            TemplateType.LOCATION.value,
            TemplateType.ROOM.value,
        ):
            raise PlaceCharacterAtPlaceError(
                f"Place type '{place_type}' cannot house characters."
            )

    def _validate_character_is_not_already_at_place(self, characters_list: List[str]):
        if self._character_identifier in characters_list:
            raise PlaceCharacterAtPlaceError(
                f"Character {self._character_identifier} is already at place {self._place_identifier}."
            )

    def execute(self) -> None:
        self._validate_character_is_not_follower()

        map_file = self._map_repository.load_map_data()

        place = map_file.get(self._place_identifier)

        if not place:
            raise ValueError(f"Place ID {self._place_identifier} not found.")

        place_type = place.get("type")

        self._validate_place_type_can_house_characters(place_type)

        characters_list = place.get("characters")

        if characters_list is None:
            characters_list = []
            place["characters"] = characters_list

        self._validate_character_is_not_already_at_place(characters_list)

        characters_list.append(self._character_identifier)

        # Save new list of characters.
        self._map_repository.save_map_data(map_file)

        logger.info(
            f"Character '{self._character_identifier}' placed at {place_type} '{self._place_identifier}'. Current character list: {characters_list}"
        )
