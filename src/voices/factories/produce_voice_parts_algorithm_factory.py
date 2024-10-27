from typing import List

from src.voices.algorithms.produce_voice_parts_algorithm import (
    ProduceVoicePartsAlgorithm,
)
from src.voices.factories.voice_part_provider_factory import VoicePartProviderFactory


class ProduceVoicePartsAlgorithmFactory:
    def __init__(self, voice_part_provider_factory: VoicePartProviderFactory):
        self._voice_part_provider_factory = voice_part_provider_factory

    def create_algorithm(
        self, text_parts: List[str], timestamp: str
    ) -> ProduceVoicePartsAlgorithm:
        return ProduceVoicePartsAlgorithm(
            text_parts, timestamp, self._voice_part_provider_factory
        )
