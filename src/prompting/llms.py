from typing import Optional

from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.prompting.llm import Llm


class Llms:
    def __init__(
        self,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        path_manager = path_manager or PathManager()

        self._llms_file = read_json_file(path_manager.get_llms_path())

        self._models = self._llms_file["models"]

    def for_story_universe_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["story_universe_generation"]])

    def for_place_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["place_generation"]])

    def for_place_description(self) -> Llm:
        return Llm(self._models[self._llms_file["place_description"]])

    def for_travel_narration(self) -> Llm:
        return Llm(self._models[self._llms_file["travel_narration"]])

    def for_speech_patterns_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["speech_patterns_generation"]])

    def for_character_connection(self) -> Llm:
        return Llm(self._models[self._llms_file["character_connection"]])

    def for_concept_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["concept_generation"]])

    def for_ambient_narration(self) -> Llm:
        return Llm(self._models[self._llms_file["ambient_narration"]])

    def for_narrative_beat(self) -> Llm:
        return Llm(self._models[self._llms_file["narrative_beat"]])

    def for_confrontation_round(self) -> Llm:
        return Llm(self._models[self._llms_file["confrontation_round"]])

    def for_grow_event(self) -> Llm:
        return Llm(self._models[self._llms_file["grow_event"]])

    def for_brainstorm_events(self) -> Llm:
        return Llm(self._models[self._llms_file["brainstorm_events"]])

    def for_character_description(self) -> Llm:
        return Llm(self._models[self._llms_file["character_description"]])

    def for_base_character_data_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["base_character_data_generation"]])

    def for_speech_turn_choice(self) -> Llm:
        return Llm(self._models[self._llms_file["speech_turn_choice"]])

    def for_speech_turn(self) -> Llm:
        return Llm(self._models[self._llms_file["speech_turn"]])

    def for_dialogue_summary(self) -> Llm:
        return Llm(self._models[self._llms_file["dialogue_summary"]])

    def for_self_reflection(self) -> Llm:
        return Llm(self._models[self._llms_file["self-reflection"]])

    def for_worldview(self) -> Llm:
        return Llm(self._models[self._llms_file["worldview"]])

    def for_action_resolution(self) -> Llm:
        return Llm(self._models[self._llms_file["action_resolution"]])

    def for_secrets_generation(self) -> Llm:
        return Llm(self._models[self._llms_file["secrets"]])

    def for_character_generation_guidelines(self) -> Llm:
        return Llm(self._models[self._llms_file["character_generation_guidelines"]])

    def for_writers_room(self) -> Llm:
        return Llm(self._models[self._llms_file["writers_room"]])

    def for_interviewee_response(self) -> Llm:
        return Llm(self._models[self._llms_file["interviewee_response"]])

    def for_place_facts(self) -> Llm:
        return Llm(self._models[self._llms_file["place_facts"]])
