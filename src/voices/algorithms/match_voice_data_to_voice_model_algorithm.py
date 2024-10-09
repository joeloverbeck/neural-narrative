import logging
from typing import Dict

from src.constants import DEFAULT_VOICE_MODEL
from src.voices.providers.matching_voice_model_provider import (
    MatchingVoiceModelProvider,
)

logger = logging.getLogger(__name__)


class MatchVoiceDataToVoiceModelAlgorithm:
    @staticmethod
    def match(voice_data: Dict[str, str]) -> str:
        product = MatchingVoiceModelProvider(voice_data).match_speaker()

        # It could be that there simply isn't a matching voice model in the list yet.
        # In that case, return a simple one that acts as narrator.
        if not product.is_valid():
            logger.warning(
                f"Couldn't find matching voice model. Error: {product.get_error()}\nProvided voice data: {voice_data}"
            )
            return DEFAULT_VOICE_MODEL

        return product.get()
