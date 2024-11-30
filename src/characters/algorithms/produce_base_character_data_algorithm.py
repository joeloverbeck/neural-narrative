from typing import Dict

from src.base.exceptions import CharacterGenerationError
from src.characters.factories.base_character_data_generation_tool_response_provider_factory import (
    BaseCharacterDataGenerationToolResponseProviderFactory,
)


class ProduceBaseCharacterDataAlgorithm:
    def __init__(
        self,
        base_data_generation_tool_response_provider_factory: BaseCharacterDataGenerationToolResponseProviderFactory,
    ):
        self._base_data_generation_tool_response_provider_factory = (
            base_data_generation_tool_response_provider_factory
        )

    def do_algorithm(self) -> Dict[str, str]:
        product = (
            self._base_data_generation_tool_response_provider_factory.create_response_provider().create_llm_response()
        )

        if not product.is_valid():
            raise CharacterGenerationError(
                f"The LLM was unable to generate a character: {product.get_error()}"
            )

        character_data = product.get()

        if "name" not in character_data:
            raise CharacterGenerationError(
                f"Failed to generate at least the character's name. Tool response: {character_data}"
            )

        return product.get()
