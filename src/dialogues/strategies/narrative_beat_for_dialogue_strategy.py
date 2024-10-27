from typing import cast

from src.base.products.text_product import TextProduct
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.factories.narrative_beat_provider_factory import (
    NarrativeBeatProviderFactory,
)
from src.dialogues.models.narrative_beat import NarrativeBeat
from src.dialogues.transcription import Transcription


class NarrativeBeatForDialogueStrategy(NarrationForDialogueStrategy):
    def __init__(
        self,
        transcription: Transcription,
        narrative_beat_provider_factory: NarrativeBeatProviderFactory,
    ):
        self._transcription = transcription
        self._narrative_beat_provider_factory = narrative_beat_provider_factory

    def produce_narration(self) -> str:
        product = cast(
            TextProduct,
            self._narrative_beat_provider_factory.create_provider(
                self._transcription
            ).generate_product(NarrativeBeat),
        )

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate narrative beat. Error: {product.get_error()}"
            )

        return product.get()
