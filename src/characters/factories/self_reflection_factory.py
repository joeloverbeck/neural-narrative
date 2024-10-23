from typing import Optional

from src.base.constants import (
    SELF_REFLECTION_GENERATION_PROMPT_FILE,
    SELF_REFLECTION_GENERATION_TOOL_FILE,
)
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.characters.products.self_reflection_product import SelfReflectionProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SelfReflectionFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        character_information_factory: CharacterInformationProvider,
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

    def _get_tool_data(self) -> dict:
        return self._filesystem_manager.load_existing_or_new_json_file(
            SELF_REFLECTION_GENERATION_TOOL_FILE
        )

    def get_user_content(self) -> str:
        return "Write a meaningful and compelling self-reflection from the first-person perspective of the character regarding their memories. Follow the provided instructions."

    def create_product_from_dict(self, arguments: dict):
        return SelfReflectionProduct(arguments.get("self_reflection"), is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        character = Character(self._playthrough_name, self._character_identifier)
        return {
            "name": character.name,
            "character_information": self._character_information_factory.get_information(),
        }
