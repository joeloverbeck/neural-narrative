import logging
import random

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.constants import MAX_CHARACTERS_TO_CREATE_AT_NEW_PLACE
from src.movements.movement_manager import MovementManager

logger = logging.getLogger(__name__)


class GenerateRandomCharactersCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        generate_character_command: GenerateCharacterCommand,
        characters_manager: CharactersManager = None,
        movement_manager: MovementManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")
        if not generate_character_command:
            raise ValueError("generate_character_command should not be empty.")

        self._playthrough_name = playthrough_name
        self._generate_character_command = generate_character_command
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )
        self._movement_manager = movement_manager or MovementManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        num_characters_to_create = random.randint(
            0, MAX_CHARACTERS_TO_CREATE_AT_NEW_PLACE
        )

        logger.info(f"Will create {num_characters_to_create} random characters.")

        for _ in range(num_characters_to_create):
            self._generate_character_command.execute()

            # Should add the latest generated character to the list of characters of the current place.
            self._movement_manager.place_character_at_current_place(
                self._characters_manager.get_latest_character_identifier()
            )
