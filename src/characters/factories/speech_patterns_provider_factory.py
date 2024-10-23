from typing import Dict

from src.characters.providers.speech_patterns_provider import SpeechPatternsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class SpeechPatternsProviderFactory:

    def __init__(
        self,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(
        self, base_character_data: Dict[str, str]
    ) -> SpeechPatternsProvider:
        return SpeechPatternsProvider(
            base_character_data, self._produce_tool_response_strategy_factory
        )
