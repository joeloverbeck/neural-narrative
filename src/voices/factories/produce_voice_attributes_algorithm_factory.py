from typing import Dict

from src.voices.algorithms.produce_voice_attributes_algorithm import (
    ProduceVoiceAttributesAlgorithm,
)
from src.voices.factories.voice_attributes_provider_factory import (
    VoiceAttributesProviderFactory,
)


class ProduceVoiceAttributesAlgorithmFactory:
    def __init__(
        self, voice_attributes_provider_factory: VoiceAttributesProviderFactory
    ):
        self._voice_attributes_provider_factory = voice_attributes_provider_factory

    def create_algorithm(
        self, base_character_data: Dict[str, str]
    ) -> ProduceVoiceAttributesAlgorithm:
        return ProduceVoiceAttributesAlgorithm(
            base_character_data, self._voice_attributes_provider_factory
        )
