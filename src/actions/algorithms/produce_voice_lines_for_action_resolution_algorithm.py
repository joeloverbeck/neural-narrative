from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.constants import NARRATOR_VOICE_MODEL
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class ProduceVoiceLinesForActionResolutionAlgorithm:
    def __init__(
        self,
        direct_voice_line_generation_algorithm_factory: DirectVoiceLineGenerationAlgorithmFactory,
    ):
        self._direct_voice_line_generation_algorithm_factory = (
            direct_voice_line_generation_algorithm_factory
        )

    def do_algorithm(self, product: ActionResolutionProduct) -> None:
        product.set_narrative_voice_line_file_name(
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                "narrator", product.get_narrative(), NARRATOR_VOICE_MODEL
            ).direct_voice_line_generation()
        )
        product.set_outcome_voice_line_file_name(
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                "narrator", product.get_outcome(), NARRATOR_VOICE_MODEL
            )
        )
