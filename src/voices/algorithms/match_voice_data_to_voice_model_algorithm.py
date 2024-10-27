import logging
from typing import Optional

from src.filesystem.config_loader import ConfigLoader
from src.voices.providers.matching_voice_model_provider import (
    MatchingVoiceModelProvider,
)
from src.voices.voice_attributes import VoiceAttributes

logger = logging.getLogger(__name__)


class MatchVoiceDataToVoiceModelAlgorithm:
    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self._config_loader = config_loader or ConfigLoader()

    def match(self, voice_attributes: VoiceAttributes) -> str:
        product = MatchingVoiceModelProvider(voice_attributes).match_speaker()
        if not product.is_valid():
            logger.warning(
                f"""Couldn't find matching voice model. Error: {product.get_error()}
Provided voice data: {voice_attributes}"""
            )

            return self._config_loader.get_default_voice_model()

        return product.get()
