from typing import Optional

from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.constants import NARRATOR_VOICE_MODEL
from src.voices.voice_manager import VoiceManager


class ProduceVoiceLinesForActionResolutionAlgorithm:
    def __init__(self, voice_manager: Optional[VoiceManager] = None):
        self._voice_manager = voice_manager or VoiceManager()

    def do_algorithm(self, product: ActionResolutionProduct) -> None:
        product.set_narrative_voice_line_file_name(
            self._voice_manager.generate_voice_line(
                "narrator", product.get_narrative(), NARRATOR_VOICE_MODEL
            )
        )
        product.set_outcome_voice_line_file_name(
            self._voice_manager.generate_voice_line(
                "narrator", product.get_outcome(), NARRATOR_VOICE_MODEL
            )
        )
        product.set_consequences_voice_line_file_name(
            self._voice_manager.generate_voice_line(
                "narrator", product.get_consequences(), NARRATOR_VOICE_MODEL
            )
        )
