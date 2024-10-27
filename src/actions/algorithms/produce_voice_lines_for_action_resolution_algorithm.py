from typing import Optional

from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.filesystem.config_loader import ConfigLoader
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class ProduceVoiceLinesForActionResolutionAlgorithm:

    def __init__(
        self,
        direct_voice_line_generation_algorithm_factory: DirectVoiceLineGenerationAlgorithmFactory,
        config_loader: Optional[ConfigLoader] = None,
    ):
        self._direct_voice_line_generation_algorithm_factory = (
            direct_voice_line_generation_algorithm_factory
        )

        self._config_loader = config_loader or ConfigLoader()

    def do_algorithm(self, product: ActionResolutionProduct) -> None:
        product.set_narrative_voice_line_file_name(
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                "narrator",
                product.get_narrative(),
                self._config_loader.get_narrator_voice_model(),
            ).direct_voice_line_generation()
        )
        product.set_outcome_voice_line_file_name(
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                "narrator",
                product.get_outcome(),
                self._config_loader.get_narrator_voice_model(),
            ).direct_voice_line_generation()
        )
