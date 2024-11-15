from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.products.text_product import TextProduct
from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class WorldviewFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        subject: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        character_information_provider_factory: CharacterInformationProviderFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(subject, "subject")

        self._playthrough_name = playthrough_name
        self._subject = subject
        self._character_information_provider_factory = (
            character_information_provider_factory
        )

        self._character = Character(self._playthrough_name, character_identifier)

    def get_prompt_file(self) -> Optional[Path]:
        return self._path_manager.get_worldview_generation_prompt_path()

    def get_user_content(self) -> str:
        return f"Write a third-person text that articulates {self._character.name}'s worldview, including their philosophical beliefs and moral standings, about the following subject: {self._subject}"

    def create_product_from_base_model(self, response_model: BaseModel):
        # have in mind that the text can come with multiple paragraphs.
        worldview = str(response_model.worldview)

        return TextProduct(worldview.replace("\n\n", "\n"), is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "name": self._character.name,
            "character_information": self._character_information_provider_factory.create_provider(
                self._subject
            ).get_information(),
        }
