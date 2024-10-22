import logging
import random
from typing import Optional
from src.base.constants import VOICE_MODELS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.products.matching_voice_model_product import MatchingVoiceModelProduct
from src.voices.voice_attributes import VoiceAttributes
logger = logging.getLogger(__name__)


class MatchingVoiceModelProvider:

    def __init__(self, voice_attributes: VoiceAttributes,
                 filesystem_manager: Optional[FilesystemManager] = None):
        self._voice_attributes = voice_attributes
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def match_speaker(self) -> MatchingVoiceModelProduct:
        """
        Matches a character's voice attributes to a suitable speaker.

        :return: The product, that if valid, will indicate a matching speaker.
        """
        voice_gender = self._voice_attributes.voice_gender
        voice_age = self._voice_attributes.voice_age
        voice_emotion = self._voice_attributes.voice_emotion
        voice_tempo = self._voice_attributes.voice_tempo
        voice_volume = self._voice_attributes.voice_volume
        voice_texture = self._voice_attributes.voice_texture
        voice_tone = self._voice_attributes.voice_tone
        voice_style = self._voice_attributes.voice_style
        voice_personality = self._voice_attributes.voice_personality
        voice_special_effects = self._voice_attributes.voice_special_effects
        attribute_checks = {'voice_gender': voice_gender, 'voice_age':
            voice_age, 'voice_emotion': voice_emotion, 'voice_tempo':
                                voice_tempo, 'voice_volume': voice_volume, 'voice_texture':
                                voice_texture, 'voice_tone': voice_tone, 'voice_style':
                                voice_style, 'voice_personality': voice_personality,
                            'voice_special_effects': voice_special_effects}
        for attr_name, attr_value in attribute_checks.items():
            if not attr_value:
                return MatchingVoiceModelProduct(None, is_valid=False,
                                                 error=f'Invalid {attr_name}.')
        possible_voice_models = (self._filesystem_manager.
                                 load_existing_or_new_json_file(VOICE_MODELS_FILE))
        attributes_in_order = [('voice_gender', voice_gender, True), (
            'voice_age', voice_age, True), ('voice_emotion', voice_emotion,
                                            False), ('voice_tempo', voice_tempo, True), ('voice_volume',
                                                                                         voice_volume, True),
                               ('voice_texture', voice_texture, True), (
                                   'voice_tone', voice_tone, False), ('voice_style', voice_style,
                                                                      False),
                               ('voice_personality', voice_personality, True), (
                                   'voice_special_effects', voice_special_effects, True)]
        for attribute_name, attribute_value, is_required in attributes_in_order:
            previous_possible_voice_models = possible_voice_models.copy()
            if attribute_value is None:
                continue
            possible_voice_models = {speaker_id: attrs for speaker_id,
            attrs in possible_voice_models.items() if attribute_value in
                                     attrs}
            if possible_voice_models:
                continue
            else:
                possible_voice_models = previous_possible_voice_models
                if is_required:
                    logger.info(
                        f'Matching voice model failed at {attribute_name}.')
                    logger.info(f'Possible voice models:\n%s',
                                possible_voice_models)
                    break
                else:
                    continue
        if not possible_voice_models:
            return MatchingVoiceModelProduct(None, is_valid=False, error=
            'No matching voice models found.')
        matched_voice_model = random.choice(list(possible_voice_models.keys()))
        return MatchingVoiceModelProduct(matched_voice_model, is_valid=True)
