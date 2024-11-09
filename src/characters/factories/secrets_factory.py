from typing import Optional

from pydantic import BaseModel

from src.characters.character import Character
from src.characters.character_memories_manager import CharacterMemoriesManager
from src.characters.products.secrets_product import SecretsProduct
from src.filesystem.path_manager import PathManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SecretsFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        path_manager: Optional[PathManager] = None,
        character_memories: Optional[CharacterMemoriesManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._places_descriptions_factory = places_descriptions_factory
        self._character_memories = character_memories or CharacterMemoriesManager(
            self._playthrough_name
        )

    def get_user_content(self) -> str:
        return "Create secrets for a character that are compelling and truly worth being hidden. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return SecretsProduct(response_model.secrets, is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return self._path_manager.get_secrets_generation_prompt_path()

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
