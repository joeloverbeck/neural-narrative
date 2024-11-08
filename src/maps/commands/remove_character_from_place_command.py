from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


class RemoveCharacterFromPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        place_identifier: str,
        place_manager_factory: PlaceManagerFactory,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(place_identifier, "place_identifier")

        self._character_identifier = character_identifier
        self._place_identifier = place_identifier
        self._place_manager_factory = place_manager_factory

        self._map_repository = map_repository or MapRepository(playthrough_name)

    def execute(self) -> None:
        place = self._place_manager_factory.create_place_manager().get_place(
            self._place_identifier
        )

        place["characters"] = [
            character_id
            for character_id in place.get("characters", [])
            if character_id != self._character_identifier
        ]

        map_file = self._map_repository.load_map_data()

        map_file[self._place_identifier] = place

        self._map_repository.save_map_data(map_file)
