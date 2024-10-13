from typing import Optional

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_information_factory import (
    CharacterInformationFactory,
)
from src.characters.products.self_reflection_product import SelfReflectionProduct
from src.constants import (
    SELF_REFLECTION_GENERATION_PROMPT_FILE,
    SELF_REFLECTION_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SelfReflectionFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        character_information_factory: CharacterInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._character_information_factory = character_information_factory

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def get_prompt_file(self) -> Optional[str]:
        return SELF_REFLECTION_GENERATION_PROMPT_FILE

    def get_tool_file(self) -> str:
        return SELF_REFLECTION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write a meaningful and compelling self-reflection from the first-person perspective of the character regarding their memories. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return SelfReflectionProduct(arguments.get("self_reflection"), is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        # Get the character's name.
        character = Character(self._playthrough_name, self._character_identifier)

        return {
            "name": character.name,
            "character_information": self._character_information_factory.get_information(),
        }
