from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    CONNECTION_GENERATION_PROMPT_FILE,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.characters.models.connection import Connection
from src.characters.products.connection_product import ConnectionProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConnectionFactory(BaseToolResponseProvider):

    def __init__(
        self,
        character_a_identifier: str,
        character_b_identifier: str,
        character_factory: CharacterFactory,
        character_information_provider_factory: CharacterInformationProviderFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._character_a_identifier = character_a_identifier
        self._character_b_identifier = character_b_identifier
        self._character_factory = character_factory
        self._character_information_provider_factory = (
            character_information_provider_factory
        )

    def _get_tool_data(self) -> dict:
        return Connection.model_json_schema()

    def get_user_content(self) -> str:
        return "Generate a meaningful and compelling connection between the two provided characters. Follow the instructions."

    def create_product_from_base_model(self, base_model: BaseModel):
        return ConnectionProduct(base_model.connection, is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return CONNECTION_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        character_a_information = (
            self._character_information_provider_factory.create_provider(
                self._character_a_identifier
            ).get_information()
        )
        character_b_information = (
            self._character_information_provider_factory.create_provider(
                self._character_b_identifier
            ).get_information()
        )

        name_a = self._character_factory.create_character(
            self._character_a_identifier
        ).name
        name_b = self._character_factory.create_character(
            self._character_b_identifier
        ).name

        return {
            "character_a_information": character_a_information,
            "character_b_information": character_b_information,
            "name_a": name_a,
            "name_b": name_b,
        }
