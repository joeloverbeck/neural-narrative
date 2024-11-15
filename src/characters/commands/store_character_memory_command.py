import logging

from src.base.abstracts.command import Command
from src.characters.character import Character
from src.databases.abstracts.database import Database

logger = logging.getLogger(__name__)


class StoreCharacterMemoryCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        memory: str,
        database: Database,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._memory = memory
        self._database = database

    def execute(self) -> None:
        character = Character(self._playthrough_name, self._character_identifier)

        self._database.insert_memory(character.identifier, self._memory)

        logger.info(
            f"Saved memory for character ({character.identifier}) '{character.name}'."
        )
