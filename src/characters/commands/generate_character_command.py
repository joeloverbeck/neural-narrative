import logging
from typing import cast, Optional

from src.base.abstracts.command import Command
from src.base.exceptions import CharacterGenerationError
from src.base.playthrough_manager import PlaythroughManager
from src.characters.characters_manager import CharactersManager
from src.characters.configs.generate_character_command_config import (
    GenerateCharacterCommandConfig,
)
from src.characters.configs.generate_character_command_factories_config import (
    GenerateCharacterCommandFactoriesConfig,
)
from src.characters.models.speech_patterns import SpeechPatterns
from src.characters.products.speech_patterns_product import SpeechPatternsProduct

logger = logging.getLogger(__name__)


class GenerateCharacterCommand(Command):

    def __init__(
        self,
        config: GenerateCharacterCommandConfig,
        factories_config: GenerateCharacterCommandFactoriesConfig,
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        self._config = config
        self._factories_config = factories_config

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._config.playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._config.playthrough_name
        )

    def execute(self) -> None:
        llm_tool_response_product = (
            self._factories_config.character_generation_tool_response_provider.create_llm_response()
        )
        if not llm_tool_response_product.is_valid():
            raise CharacterGenerationError(
                f"The LLM was unable to generate a character: {llm_tool_response_product.get_error()}"
            )

        character_data = llm_tool_response_product.get()

        if "name" not in character_data:
            raise CharacterGenerationError(
                f"Failed to generate at least the character's name. Tool response: {character_data}"
            )

        product = cast(
            SpeechPatternsProduct,
            self._factories_config.speech_patterns_provider_factory.create_provider(
                character_data
            ).generate_product(SpeechPatterns),
        )

        if not product.is_valid():
            raise CharacterGenerationError(
                f"The LLM failed to produce valid speech patterns. Error: {product.get_error()}"
            )
        character_data.update({"speech_patterns": product.get()})

        self._factories_config.store_generate_character_command_factory.create_store_generated_character_command(
            character_data
        ).execute()
        self._factories_config.generate_character_image_command_factory.create_command(
            self._characters_manager.get_latest_character_identifier()
        ).execute()

        if self._config.place_character_at_current_place:
            current_place = self._playthrough_manager.get_current_place_identifier()
            self._factories_config.place_character_at_place_command_factory.create_command(
                self._characters_manager.get_latest_character_identifier(),
                current_place,
            ).execute()
