import logging

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
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
        store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        place_character_at_current_place: bool,
        characters_manager: CharactersManager = None,
        movement_manager: MovementManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._character_generation_tool_response_provider = (
            character_generation_tool_response_provider
        )
        self._store_generate_character_command_factory = (
            store_generate_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )
        self._place_character_at_current_place = place_character_at_current_place

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._movement_manager = movement_manager or MovementManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        llm_tool_response_product = (
            self._character_generation_tool_response_provider.create_llm_response()
        )

        if not llm_tool_response_product.is_valid():
            logger.error(
                f"The LLM was unable to generate a character: {llm_tool_response_product.get_error()}"
            )
            return

        print(f"Produced character: {llm_tool_response_product.get()}")

        self._store_generate_character_command_factory.create_store_generated_character_command(
            llm_tool_response_product.get()
        ).execute()

        # Now that the character is stored, we need to retrieve the latest character identifier,
        # then use it to generate the character image
        self._generate_character_image_command_factory.create_generate_character_image_command(
            self._characters_manager.get_latest_character_identifier()
        ).execute()

        if self._place_character_at_current_place:
            # The user (usually me) likely wants to place the newly created character at the current place.
            self._movement_manager.place_character_at_current_place(
                self._characters_manager.get_latest_character_identifier()
            )
