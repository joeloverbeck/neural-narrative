from src.base.validators import validate_non_empty_string
from src.movements.commands.place_character_at_place_command import (
    PlaceCharacterAtPlaceCommand,
)


class PlaceCharacterAtPlaceCommandFactory:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def create_command(
        self, character_identifier: str, place_identifier: str
    ) -> PlaceCharacterAtPlaceCommand:
        return PlaceCharacterAtPlaceCommand(
            self._playthrough_name, character_identifier, place_identifier
        )
