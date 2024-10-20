from typing import Optional

from src.base.enums import TemplateType
from src.base.required_string import RequiredString
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)


class CreateMapEntryForPlaythroughCommandProvider:

    def __init__(
        self,
            playthrough_name: RequiredString,
            father_identifier: Optional[RequiredString],
            place_type: TemplateType,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type

    def create_command(
            self, place_template: RequiredString
    ) -> CreateMapEntryForPlaythroughCommand:
        if not place_template:
            raise ValueError("place_template can't be empty.")

        return CreateMapEntryForPlaythroughCommand(
            self._playthrough_name,
            self._father_identifier,
            self._place_type,
            place_template,
        )
