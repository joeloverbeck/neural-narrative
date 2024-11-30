import logging
from typing import Dict, Any

from src.base.abstracts.command import Command
from src.characters.configs.generate_character_command_factories_config import (
    GenerateCharacterCommandFactoriesConfig,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommand(Command):

    def __init__(
        self,
        is_player: bool,
        factories_config: GenerateCharacterCommandFactoriesConfig,
    ):
        self._is_player = is_player
        self._factories_config = factories_config

    def execute(self) -> None:
        character_data: Dict[str, Any] = {}

        # First generate the base character data.
        base_character_data = (
            self._factories_config.produce_base_character_data_algorithm_factory.create_algorithm().do_algorithm()
        )

        character_data.update(base_character_data)

        # Now generate the voice attributes.
        voice_attributes_data = self._factories_config.produce_voice_attributes_algorithm_factory.create_algorithm(
            base_character_data
        ).do_algorithm()

        character_data.update(voice_attributes_data)

        # Now generate the speech patterns.
        speech_patterns = self._factories_config.produce_speech_patterns_algorithm_factory.create_algorithm(
            character_data
        ).do_algorithm()

        character_data.update({"speech_patterns": speech_patterns})

        self._factories_config.process_generated_character_data_command_factory.create_command(
            character_data, place_character_at_current_place=not self._is_player
        ).execute()
