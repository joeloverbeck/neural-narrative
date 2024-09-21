import logging
import random

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.enums import CharacterGenerationType
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.constants import MAX_CHARACTERS_TO_CREATE_AT_NEW_PLACE
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.movements.movement_manager import MovementManager

logger = logging.getLogger(__name__)


class GenerateRandomCharactersCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        places_templates_parameter: PlacesTemplatesParameter,
        generate_character_command_factory: GenerateCharacterCommandFactory,
        characters_manager: CharactersManager = None,
        movement_manager: MovementManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name
        self._places_templates_parameter = places_templates_parameter
        self._generate_character_command_factory = generate_character_command_factory
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )
        self._movement_manager = movement_manager or MovementManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        num_characters_to_create = random.randint(
            1, MAX_CHARACTERS_TO_CREATE_AT_NEW_PLACE
        )

        logger.info(f"Will create {num_characters_to_create} random characters.")

        for _ in range(num_characters_to_create):
            self._generate_character_command_factory.create_generate_character_command(
                self._places_templates_parameter,
                place_character_at_current_place=True,
                character_generation_type=CharacterGenerationType.AUTOMATIC,
            ).execute()
