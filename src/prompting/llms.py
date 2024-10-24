from typing import Optional

from src.base.constants import LLMS_FILE
from src.filesystem.filesystem_manager import FilesystemManager


class Llms:
    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        self._llms_file = self._filesystem_manager.load_existing_or_new_json_file(
            LLMS_FILE
        )

        self._models = self._llms_file["models"]

    def for_story_universe_generation(self) -> str:
        return self._models[self._llms_file["story_universe_generation"]]

    def for_place_generation(self) -> str:
        return self._models[self._llms_file["place_generation"]]

    def for_place_description(self) -> str:
        return self._models[self._llms_file["place_description"]]

    def for_travel_narration(self) -> str:
        return self._models[self._llms_file["travel_narration"]]

    def for_speech_patterns_generation(self) -> str:
        return self._models[self._llms_file["speech_patterns_generation"]]

    def for_character_connection(self) -> str:
        return self._models[self._llms_file["character_connection"]]

    def for_concept_generation(self) -> str:
        return self._models[self._llms_file["concept_generation"]]

    def for_ambient_narration(self) -> str:
        return self._models[self._llms_file["ambient_narration"]]

    def for_character_description(self) -> str:
        return self._models[self._llms_file["character_description"]]

    def for_base_character_data_generation(self) -> str:
        return self._models[self._llms_file["base_character_data_generation"]]

    def for_speech_turn_choice(self) -> str:
        return self._models[self._llms_file["speech_turn_choice"]]

    def for_speech_turn(self) -> str:
        return self._models[self._llms_file["speech_turn"]]

    def for_dialogue_summary(self) -> str:
        return self._models[self._llms_file["dialogue_summary"]]

    def for_self_reflection(self) -> str:
        return self._models[self._llms_file["self-reflection"]]

    def for_action_resolution(self) -> str:
        return self._models[self._llms_file["action_resolution"]]

    def for_secrets_generation(self):
        return self._models[self._llms_file["secrets"]]

    def for_character_generation_guidelines(self) -> str:
        return self._models[self._llms_file["character_generation_guidelines"]]
