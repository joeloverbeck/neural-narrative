from typing import List, cast, Dict

from src.base.exceptions import CharacterGenerationError
from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)
from src.characters.models.speech_patterns import SpeechPatterns
from src.characters.products.speech_patterns_product import SpeechPatternsProduct


class ProduceSpeechPatternsAlgorithm:
    def __init__(
        self,
        character_data: Dict[str, str],
        speech_patterns_provider_factory: SpeechPatternsProviderFactory,
    ):
        self._character_data = character_data
        self._speech_patterns_provider_factory = speech_patterns_provider_factory

    def do_algorithm(self) -> List[str]:
        product = cast(
            SpeechPatternsProduct,
            self._speech_patterns_provider_factory.create_provider(
                self._character_data
            ).generate_product(SpeechPatterns),
        )

        if not product.is_valid():
            raise CharacterGenerationError(
                f"The LLM failed to produce valid speech patterns. Error: {product.get_error()}"
            )

        return product.get()
