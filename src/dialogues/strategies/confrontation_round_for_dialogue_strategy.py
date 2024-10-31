from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.factories.confrontation_round_provider_factory import (
    ConfrontationRoundProviderFactory,
)
from src.dialogues.models.confrontation_round import ConfrontationRound
from src.dialogues.transcription import Transcription


class ConfrontationRoundForDialogueStrategy(NarrationForDialogueStrategy):
    def __init__(
        self,
        transcription: Transcription,
        confrontation_round_provider_factory: ConfrontationRoundProviderFactory,
    ):
        self._transcription = transcription
        self._confrontation_round_provider_factory = (
            confrontation_round_provider_factory
        )

    def produce_narration(self) -> str:
        product = self._confrontation_round_provider_factory.create_provider(
            self._transcription
        ).generate_product(ConfrontationRound)

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate confrontation round. Error: {product.get_error()}"
            )

        return product.get()
