from typing import Optional

from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import TemplateType
from src.maps.providers.create_map_entry_for_playthrough_command_provider import (
    CreateMapEntryForPlaythroughCommandProvider,
)


class CreateMapEntryForPlaythroughCommandProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        produce_and_update_next_identifier: ProduceAndUpdateNextIdentifierAlgorithm,
    ):
        self._playthrough_name = playthrough_name
        self._produce_and_update_next_identifier = produce_and_update_next_identifier

    def create_provider(
        self, father_identifier: Optional[str], place_type: TemplateType
    ) -> CreateMapEntryForPlaythroughCommandProvider:
        return CreateMapEntryForPlaythroughCommandProvider(
            self._playthrough_name,
            father_identifier,
            place_type,
            self._produce_and_update_next_identifier,
        )
