from typing import Optional, Dict, Any, List

from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager


class LlmsRepository:

    def __init__(self, path_manager: Optional[PathManager] = None):

        self._path_manager = path_manager or PathManager()

        self._llms_path = self._path_manager.get_llms_path()

    def _load_llms_data(self) -> Dict[str, Any]:
        return read_json_file(self._llms_path)

    def _get_assigned_llm(self, action_type: str) -> str:
        return self._load_llms_data()[action_type]

    def get_action_types(self) -> List[str]:
        """Get the list of action types (keys in llms_data excluding 'models')"""
        return [key for key in self._load_llms_data().keys() if key != "models"]

    @staticmethod
    def get_action_type_category(action_type: str) -> str:
        action_type_categories = {
            "story_universe_generation": "places",
            "place_generation": "places",
            "place_description": "places",
            "travel_narration": "places",
            "character_generation_guidelines": "characters",
            "base_character_data_generation": "characters",
            "speech_patterns_generation": "characters",
            "character_description": "characters",
            "self-reflection": "characters",
            "worldview": "characters",
            "character_connection": "characters",
            "secrets": "characters",
            "concept_generation": "concepts",
            "writers_room": "concepts",
            "ambient_narration": "dialogues",
            "narrative_beat": "dialogues",
            "grow_event": "dialogues",
            "confrontation_round": "dialogues",
            "speech_turn_choice": "dialogues",
            "speech_turn": "dialogues",
            "dialogue_summary": "dialogues",
            "action_resolution": "actions",
            "interviewee_response": "interviews",
        }

        return action_type_categories.get(action_type, "characters")

    def get_models(self) -> Dict[str, Dict[str, Any]]:
        return self._load_llms_data()["models"]

    def assign_llm(self, action_type: str, llm_key: str) -> None:
        llms_data = self._load_llms_data()

        llms_data[action_type] = llm_key

        write_json_file(self._llms_path, llms_data)

    def has_llm_assigned(self, action_type: str, llm_key: str) -> bool:
        return self._get_assigned_llm(action_type) == llm_key
