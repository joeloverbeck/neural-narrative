from typing import cast

from src.base.products.text_product import TextProduct
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.factories.grow_event_provider_factory import GrowEventProviderFactory
from src.dialogues.models.grow_event import GrowEvent
from src.dialogues.transcription import Transcription


class GrowEventNarrationForDialogueStrategy(NarrationForDialogueStrategy):
    def __init__(
            self,
            transcription: Transcription,
            grow_event_provider_factory: GrowEventProviderFactory,
    ):
        self._transcription = transcription
        self._grow_event_provider_factory = grow_event_provider_factory

    def produce_narration(self) -> str:
        product = cast(
            TextProduct,
            self._grow_event_provider_factory.create_provider(
                self._transcription
            ).generate_product(GrowEvent),
        )

        if not product.is_valid():
            raise ValueError(f"Was unable to grow event. Error: {product.get_error()}")

        return product.get()
