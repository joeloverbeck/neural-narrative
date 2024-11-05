import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.products.text_product import TextProduct
from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class SelfReflectionFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        character_information_factory: CharacterInformationProvider,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            produce_tool_response_strategy_factory, filesystem_manager, path_manager
        )

        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._character_information_factory = character_information_factory

    def get_prompt_file(self) -> Optional[Path]:
        return self._path_manager.get_self_reflection_generation_prompt_path()

    def get_user_content(self) -> str:
        return "Write a meaningful and compelling self-reflection from the first-person perspective of the character regarding their memories. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        logger.info(
            f"Self-reflection reasoning: %s",
            response_model.self_reflection.chain_of_thought,
        )

        # have in mind that the self-reflection can come with multiple paragraphs.
        self_reflection = str(response_model.self_reflection.reflection)

        return TextProduct(self_reflection.replace("\n\n", "\n"), is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        character = Character(self._playthrough_name, self._character_identifier)

        return {
            "name": character.name,
            "character_information": self._character_information_factory.get_information(),
        }
