import logging
from typing import cast

from src.base.abstracts.command import Command
from src.base.exceptions import CharacterGenerationError
from src.characters.characters_manager import CharactersManager
from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.characters.products.speech_patterns_product import SpeechPatternsProduct
from src.characters.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.movement_manager import MovementManager

logger = logging.getLogger(__name__)


class GenerateCharacterCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_generation_tool_response_provider: CharacterGenerationToolResponseProvider,
        speech_patterns_provider_factory: SpeechPatternsProviderFactory,
        store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        place_character_at_current_place: bool,
        movement_manager: MovementManager,
        characters_manager: CharactersManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_generation_tool_response_provider = (
            character_generation_tool_response_provider
        )
        self._speech_patterns_provider_factory = speech_patterns_provider_factory
        self._store_generate_character_command_factory = (
            store_generate_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )
        self._place_character_at_current_place = place_character_at_current_place
        self._movement_manager = movement_manager
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        llm_tool_response_product = (
            self._character_generation_tool_response_provider.create_llm_response()
        )
        if not llm_tool_response_product.is_valid():
            raise CharacterGenerationError(
                f"The LLM was unable to generate a character: {llm_tool_response_product.get_error()}"
            )
        character_data = llm_tool_response_product.get()
        if "name" not in character_data:
            raise CharacterGenerationError(
                f"""Failed to generate at least the character's name. Tool response:
{character_data}"""
            )
        product = cast(
            SpeechPatternsProduct,
            self._speech_patterns_provider_factory.create_provider(
                character_data
            ).generate_product(),
        )
        if not product.is_valid():
            raise CharacterGenerationError(
                f"The LLM failed to produce valid speech patterns. Error: {product.get_error()}"
            )
        character_data.update({"speech_patterns": product.get()})
        self._store_generate_character_command_factory.create_store_generated_character_command(
            character_data
        ).execute()
        self._generate_character_image_command_factory.create_command(
            self._characters_manager.get_latest_character_identifier()
        ).execute()
        if self._place_character_at_current_place:
            self._movement_manager.place_character_at_current_place(
                self._characters_manager.get_latest_character_identifier()
            )
