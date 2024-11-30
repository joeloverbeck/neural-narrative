from typing import Dict

from src.characters.algorithms.produce_speech_patterns_algorithm import (
    ProduceSpeechPatternsAlgorithm,
)
from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)


class ProduceSpeechPatternsAlgorithmFactory:
    def __init__(self, speech_patterns_provider_factory: SpeechPatternsProviderFactory):
        self._speech_patterns_provider_factory = speech_patterns_provider_factory

    def create_algorithm(
        self, character_data: Dict[str, str]
    ) -> ProduceSpeechPatternsAlgorithm:
        return ProduceSpeechPatternsAlgorithm(
            character_data, self._speech_patterns_provider_factory
        )
