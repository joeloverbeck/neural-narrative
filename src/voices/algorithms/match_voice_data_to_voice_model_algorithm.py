import logging
from src.base.constants import DEFAULT_VOICE_MODEL
from src.voices.providers.matching_voice_model_provider import MatchingVoiceModelProvider
from src.voices.voice_attributes import VoiceAttributes
logger = logging.getLogger(__name__)


class MatchVoiceDataToVoiceModelAlgorithm:

    @staticmethod
    def match(voice_attributes: VoiceAttributes) -> str:
        product = MatchingVoiceModelProvider(voice_attributes).match_speaker()
        if not product.is_valid():
            logger.warning(
                f"""Couldn't find matching voice model. Error: {product.get_error()}
Provided voice data: {voice_attributes}"""
            )
            return DEFAULT_VOICE_MODEL
        return product.get()
