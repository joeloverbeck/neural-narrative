from typing import cast

from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.factories.ambient_narration_provider_factory import (
    AmbientNarrationProviderFactory,
)
from src.dialogues.models.ambient_narration import AmbientNarration
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription


class AmbientNarrationForDialogueStrategy(NarrationForDialogueStrategy):
    def __init__(
        self,
        transcription: Transcription,
        ambient_narration_provider_factory: AmbientNarrationProviderFactory,
    ):
        self._transcription = transcription
        self._ambient_narration_provider_factory = ambient_narration_provider_factory

    def produce_narration(self) -> str:
        product = cast(
            AmbientNarrationProduct,
            self._ambient_narration_provider_factory.create_provider(
                self._transcription
            ).generate_product(AmbientNarration),
        )

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate ambient narration. Error: {product.get_error()}"
            )

        return product.get()
