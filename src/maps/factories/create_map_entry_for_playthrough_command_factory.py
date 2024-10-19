from typing import Optional

from src.base.enums import PlaceType
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)


class CreateMapEntryForPlaythroughCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        father_identifier: Optional[str],
        place_type: PlaceType,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type

    def create_command(
        self, place_template: str
    ) -> CreateMapEntryForPlaythroughCommand:
        if not place_template:
            raise ValueError("place_template can't be empty.")

        return CreateMapEntryForPlaythroughCommand(
            self._playthrough_name,
            self._father_identifier,
            self._place_type,
            place_template,
        )
