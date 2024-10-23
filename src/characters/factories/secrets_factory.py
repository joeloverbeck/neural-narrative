from typing import Optional

from src.base.constants import (
    SECRETS_GENERATION_PROMPT_FILE,
    SECRETS_GENERATION_TOOL_FILE,
)
from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.characters.products.secrets_product import SecretsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SecretsFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        produce_tool_response_strategy_factory: UnparsedStringProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        filesystem_manager: Optional[FilesystemManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._places_descriptions_factory = places_descriptions_factory
        self._character_memories = character_memories or CharacterMemories(
            self._playthrough_name
        )

    def _get_tool_data(self) -> dict:
        return self._filesystem_manager.load_existing_or_new_json_file(
            SECRETS_GENERATION_TOOL_FILE
        )

    def get_user_content(self) -> str:
        return "Create secrets for a character that are compelling and truly worth being hidden. Follow the provided instructions."

    def create_product_from_dict(self, arguments: dict):
        secrets = arguments.get("secrets")
        if not secrets:
            raise ValueError("The LLM didn't produce valid secrets.")
        return SecretsProduct(secrets, is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return SECRETS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "places_descriptions": self._places_descriptions_factory.get_information()
        }
        character = Character(self._playthrough_name, self._character_identifier)
        prompt_data.update(
            {
                "name": character.name,
                "description": character.description,
                "personality": character.personality,
                "profile": character.profile,
                "likes": character.likes,
                "dislikes": character.dislikes,
                "secrets": character.secrets,
                "speech_patterns": character.speech_patterns,
                "health": character.health,
                "equipment": character.equipment,
            }
        )
        memories = self._character_memories.load_memories(character)
        prompt_data.update({"memories": memories})
        return prompt_data
