from typing import Dict

from src.characters.providers.speech_patterns_provider import SpeechPatternsProvider
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)


class SpeechPatternsProviderFactory:

    def __init__(
        self,
        produce_tool_response_strategy_factory: UnparsedStringProduceToolResponseStrategyFactory,
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
