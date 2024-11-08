from src.base.validators import validate_non_empty_string
from src.maps.commands.remove_character_from_place_command import (
    RemoveCharacterFromPlaceCommand,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class RemoveCharacterFromPlaceCommandFactory:
    def __init__(
        self, playthrough_name: str, place_manager_factory: PlaceManagerFactory
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._place_manager_factory = place_manager_factory

    def create_command(
        self, character_identifier: str, place_identifier: str
    ) -> RemoveCharacterFromPlaceCommand:
        return RemoveCharacterFromPlaceCommand(
            self._playthrough_name,
            character_identifier,
            place_identifier,
            self._place_manager_factory,
        )
