from typing import Optional

from src.base.enums import TemplateType
from src.base.required_string import RequiredString
from src.maps.providers.create_map_entry_for_playthrough_command_provider import (
    CreateMapEntryForPlaythroughCommandProvider,
)


class CreateMapEntryForPlaythroughCommandProviderFactory:

    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_provider(
            self, father_identifier: Optional[RequiredString], place_type: TemplateType
    ) -> CreateMapEntryForPlaythroughCommandProvider:
        return CreateMapEntryForPlaythroughCommandProvider(
            self._playthrough_name, father_identifier, place_type
        )
