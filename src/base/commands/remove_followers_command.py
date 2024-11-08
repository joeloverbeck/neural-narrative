from typing import List, Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string, validate_list_of_str
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


class RemoveFollowersCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        follower_identifiers: List[str],
        place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_list_of_str(follower_identifiers)

        self._follower_identifiers = follower_identifiers
        self._place_character_at_place_command_factory = (
            place_character_at_place_command_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def execute(self) -> None:
        for follower_id in self._follower_identifiers:
            self._playthrough_manager.remove_follower(follower_id)
            self._place_character_at_place_command_factory.create_command(
                follower_id, self._playthrough_manager.get_current_place_identifier()
            ).execute()
