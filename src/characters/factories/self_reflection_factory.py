from typing import Optional

from src.characters.characters_manager import CharactersManager
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
        # Load the character memories.
        memories = self._characters_manager.load_character_memories(
            self._character_identifier
        )

        # Get the character's name.
        character_data = self._characters_manager.load_character_data(
            self._character_identifier
        )

        return {
            "name": character_data["name"],
            "description": character_data["description"],
            "personality": character_data["personality"],
            "profile": character_data["profile"],
            "likes": character_data["likes"],
            "dislikes": character_data["dislikes"],
            "speech_patterns": character_data["speech patterns"],
            "health": character_data["health"],
            "equipment": character_data["equipment"],
            "memories": memories,
        }
