from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    CHARACTER_DESCRIPTION_GENERATION_PROMPT_FILE,
)
from src.characters.character import Character
from src.characters.products.character_description_product import (
    CharacterDescriptionProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class CharacterDescriptionProvider(BaseToolResponseProvider):

    def __init__(
        self,
        character: Character,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._character = character

    def get_prompt_file(self) -> Optional[str]:
        return CHARACTER_DESCRIPTION_GENERATION_PROMPT_FILE

    def get_user_content(self) -> str:
        return "Craft a detailed and vivid description of the character's appearance suitable for an image-generating AI, as per the above instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return CharacterDescriptionProduct(response_model.description, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "name": self._character.name,
            "description": self._character.description,
            "personality": self._character.personality,
            "health": self._character.health,
            "equipment": self._character.equipment,
        }
