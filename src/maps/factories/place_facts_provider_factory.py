from src.dialogues.providers.place_facts_provider import PlaceFactsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class PlaceFactsProviderFactory:
    def __init__(
        self, produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(self, place_description: str) -> PlaceFactsProvider:
        return PlaceFactsProvider(
            place_description, self._produce_tool_response_strategy_factory
        )
