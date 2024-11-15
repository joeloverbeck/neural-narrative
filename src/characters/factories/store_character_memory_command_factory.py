from src.base.validators import validate_non_empty_string
from src.characters.commands.store_character_memory_command import (
    StoreCharacterMemoryCommand,
)
from src.databases.abstracts.database import Database


class StoreCharacterMemoryCommandFactory:

    def __init__(self, playthrough_name: str, database: Database):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._database = database

    def create_store_character_memory_command(
        self, participant_identifier: str, memory: str
    ) -> StoreCharacterMemoryCommand:
        return StoreCharacterMemoryCommand(
            self._playthrough_name, participant_identifier, memory, self._database
        )
