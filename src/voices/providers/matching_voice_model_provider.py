import random
from typing import Dict, Optional

from src.constants import VOICE_MODELS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.products.matching_voice_model_product import MatchingVoiceModelProduct


class MatchingVoiceModelProvider:

    def __init__(
        self,
        character_voice_attributes: Dict[str, str],
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._character_voice_attributes = character_voice_attributes

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def match_speaker(self) -> MatchingVoiceModelProduct:
        """
        Matches a character's voice attributes to a suitable speaker.

        :return: The product, that if valid, will indicate a matching speaker.
        """
        # Extract character's voice attributes
        voice_gender = self._character_voice_attributes.get("voice_gender")
        voice_age = self._character_voice_attributes.get("voice_age")
        voice_emotion = self._character_voice_attributes.get("voice_emotion")
        voice_tempo = self._character_voice_attributes.get("voice_tempo")
        voice_volume = self._character_voice_attributes.get("voice_volume")
        voice_texture = self._character_voice_attributes.get("voice_texture")
        voice_style = self._character_voice_attributes.get("voice_style")
        voice_personality = self._character_voice_attributes.get("voice_personality")
        voice_special_effects = self._character_voice_attributes.get(
            "voice_special_effects"
        )

        # None of the voice attributes should be invalid.
        if not voice_gender:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_gender."
            )
        if not voice_age:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_age."
            )
        if not voice_emotion:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_emotion."
            )
        if not voice_tempo:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_tempo."
            )
        if not voice_volume:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_volume."
            )
        if not voice_texture:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_texture."
            )
        if not voice_style:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_style."
            )
        if not voice_personality:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_personality."
            )
        if not voice_special_effects:
            return MatchingVoiceModelProduct(
                None, is_valid=False, error="Invalid voice_special_effects."
            )

        # Initialize the list of possible speakers
        possible_voice_models = self._filesystem_manager.load_existing_or_new_json_file(
            VOICE_MODELS_FILE
        )

        attributes_in_order = [
            ("voice_gender", voice_gender, True),
            ("voice_age", voice_age, True),
            ("voice_emotion", voice_emotion, False),
            ("voice_tempo", voice_tempo, True),
            ("voice_volume", voice_volume, False),
            ("voice_texture", voice_texture, True),
            ("voice_style", voice_style, False),
            ("voice_personality", voice_personality, True),
            ("voice_special_effects", voice_special_effects, True),
        ]

        for attribute_name, attribute_value, is_required in attributes_in_order:
            previous_possible_voice_models = possible_voice_models.copy()

            # Skip filtering if attribute value is None
            if attribute_value is None:
                continue

            # Filter possible_voice_models
            possible_voice_models = {
                speaker_id: attrs
                for speaker_id, attrs in possible_voice_models.items()
                if attribute_value in attrs
            }

            if possible_voice_models:
                continue
            else:
                # No voice models match the attribute
                possible_voice_models = previous_possible_voice_models

                if is_required:
                    # Stop further filtering and break the loop
                    break
                else:
                    # For optional attribute, continue with previous_possible_voice_models
                    continue

        if not possible_voice_models:
            # If possible_voice_models is empty, return invalid product
            return MatchingVoiceModelProduct(
                None,
                is_valid=False,
                error="No matching voice models found.",
            )

        # Randomly select a speaker from the remaining list
        matched_voice_model = random.choice(list(possible_voice_models.keys()))

        return MatchingVoiceModelProduct(matched_voice_model, is_valid=True)
