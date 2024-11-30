from typing import Dict, cast

from src.base.exceptions import CharacterGenerationError
from src.base.products.dict_product import DictProduct
from src.voices.factories.voice_attributes_provider_factory import (
    VoiceAttributesProviderFactory,
)
from src.voices.models.voice_attributes import VoiceAttributes


class ProduceVoiceAttributesAlgorithm:

    def __init__(
        self,
        base_character_data: Dict[str, str],
        voice_attributes_provider_factory: VoiceAttributesProviderFactory,
    ):
        self._base_character_data = base_character_data
        self._voice_attributes_provider_factory = voice_attributes_provider_factory

    def do_algorithm(self) -> Dict[str, str]:
        product = cast(
            DictProduct,
            self._voice_attributes_provider_factory.create_provider(
                self._base_character_data
            ).generate_product(VoiceAttributes),
        )

        if not product.is_valid():
            raise CharacterGenerationError(
                f"Was unable to produce voice attributes for character '{self._base_character_data["name"]}'. Error: {product.get_error()}"
            )

        # The product is valid.
        return product.get()
