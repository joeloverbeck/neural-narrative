from typing import Optional

from pydantic import BaseModel

from src.base.tools import join_with_newline
from src.characters.composers.character_information_provider_factory_composer import (
    CharacterInformationProviderFactoryComposer,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.products.connection_product import ConnectionProduct
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.filesystem.path_manager import PathManager
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
        character_information_provider_factory_composer: CharacterInformationProviderFactoryComposer,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._character_a_identifier = character_a_identifier
        self._character_b_identifier = character_b_identifier
        self._character_factory = character_factory
        self._character_information_provider_factory_composer = (
            character_information_provider_factory_composer
        )
        self._format_known_facts_algorithm = format_known_facts_algorithm

    def get_user_content(self) -> str:
        return "Generate a meaningful and compelling connection between the two provided characters. Follow the instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return ConnectionProduct(response_model.connection, is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return self._path_manager.get_connection_generation_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        name_a = self._character_factory.create_character(
            self._character_a_identifier
        ).name
        name_b = self._character_factory.create_character(
            self._character_b_identifier
        ).name

        character_a_information = (
            self._character_information_provider_factory_composer.compose_factory(
                self._character_a_identifier
            )
            .create_provider(name_b)
            .get_information()
        )
        character_b_information = (
            self._character_information_provider_factory_composer.compose_factory(
                self._character_b_identifier
            )
            .create_provider(name_a)
            .get_information()
        )

        return {
            "character_a_information": character_a_information,
            "character_b_information": character_b_information,
            "name_a": name_a,
            "name_b": name_b,
            "known_facts": self._format_known_facts_algorithm.do_algorithm(
                join_with_newline(character_a_information, character_b_information)
            ),
        }
