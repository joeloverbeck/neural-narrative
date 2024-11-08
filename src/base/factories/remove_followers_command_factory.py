from typing import List

from src.base.commands.remove_followers_command import RemoveFollowersCommand
from src.base.validators import validate_non_empty_string
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


class RemoveFollowersCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._place_character_at_place_command_factory = (
            place_character_at_place_command_factory
        )

        self._playthrough_name = playthrough_name

    def create_command(self, follower_identifiers: List[str]) -> RemoveFollowersCommand:
        return RemoveFollowersCommand(
            self._playthrough_name,
            follower_identifiers,
            self._place_character_at_place_command_factory,
        )
