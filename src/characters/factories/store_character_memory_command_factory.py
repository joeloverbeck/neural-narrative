from src.base.required_string import RequiredString
from src.characters.commands.store_character_memory_command import (
    StoreCharacterMemoryCommand,
)


class StoreCharacterMemoryCommandFactory:
    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_store_character_memory_command(
        self, participant_identifier: RequiredString, memory: RequiredString
    ) -> StoreCharacterMemoryCommand:
        return StoreCharacterMemoryCommand(
            self._playthrough_name, participant_identifier, memory
        )
