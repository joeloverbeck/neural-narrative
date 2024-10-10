from src.characters.providers.character_description_provider import (
    CharacterDescriptionProvider,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class CharacterDescriptionProviderFactory:
    def __init__(
        self, produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(self, character_data: dict):
        if "health" not in character_data:
            raise ValueError("health should have been present in character_data.")

        return CharacterDescriptionProvider(
            character_data, self._produce_tool_response_strategy_factory
        )
