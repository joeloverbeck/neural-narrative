from typing import Optional

from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.commands.create_map_entry_for_playthrough_command import (
    CreateMapEntryForPlaythroughCommand,
)


class CreateMapEntryForPlaythroughCommandProvider:

    def __init__(
        self,
        playthrough_name: str,
        father_identifier: Optional[str],
        place_type: TemplateType,
        produce_and_update_next_identifier: ProduceAndUpdateNextIdentifierAlgorithm,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type
        self._produce_and_update_next_identifier = produce_and_update_next_identifier

    def create_command(
        self, place_template: str
    ) -> CreateMapEntryForPlaythroughCommand:
        validate_non_empty_string(place_template, "place_template")
        return CreateMapEntryForPlaythroughCommand(
            self._playthrough_name,
            self._father_identifier,
            self._place_type,
            place_template,
            self._produce_and_update_next_identifier,
        )
