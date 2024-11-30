from typing import Dict

from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.voices.providers.voice_attributes_provider import VoiceAttributesProvider


class VoiceAttributesProviderFactory:
    def __init__(
        self, produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(
        self, base_character_data: Dict[str, str]
    ) -> VoiceAttributesProvider:
        return VoiceAttributesProvider(
            base_character_data, self._produce_tool_response_strategy_factory
        )
