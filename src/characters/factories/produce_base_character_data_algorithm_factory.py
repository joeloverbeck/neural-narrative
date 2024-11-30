from src.characters.algorithms.produce_base_character_data_algorithm import (
    ProduceBaseCharacterDataAlgorithm,
)
from src.characters.factories.base_character_data_generation_tool_response_provider_factory import (
    BaseCharacterDataGenerationToolResponseProviderFactory,
)


class ProduceBaseCharacterDataAlgorithmFactory:

    def __init__(
        self,
        base_data_generation_tool_response_provider_factory: BaseCharacterDataGenerationToolResponseProviderFactory,
    ):
        self._base_data_generation_tool_response_provider_factory = (
            base_data_generation_tool_response_provider_factory
        )

    def create_algorithm(self) -> ProduceBaseCharacterDataAlgorithm:
        return ProduceBaseCharacterDataAlgorithm(
            self._base_data_generation_tool_response_provider_factory
        )
