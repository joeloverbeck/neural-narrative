# src.filesystem.config_loader.py

from pathlib import Path
from typing import Optional

from src.filesystem.file_operations import read_file, read_json_file
from src.filesystem.path_manager import PathManager


class ConfigLoader:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

        # load the config file.
        self._config = read_json_file(self._path_manager.get_config_path())

    @staticmethod
    def _load_secret_key(file_path: Path) -> str:
        try:
            return read_file(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Secret key file '{file_path}' not found.")
        except Exception as e:
            raise Exception(f"An error occurred while loading '{file_path}': {str(e)}")

    def _crash_if_config_key_missing(self, key: str):
        if not key in self._config:
            raise KeyError(f"The config file didn't contain an entry for '{key}'.")

    def _get_config_key(self, key: str):
        self._crash_if_config_key_missing(key)

        return self._config[key]

    def get_produce_voice_lines(self) -> bool:
        return self._get_config_key("produce_voice_lines")

    def get_produce_player_voice_lines(self) -> bool:
        return self._get_config_key("produce_player_voice_lines")

    def get_generate_character_guidelines_on_first_visit(self) -> bool:
        return self._get_config_key("generate_character_guidelines_on_first_visit")

    def get_augment_context_for_speech(self) -> str:
        return self._get_config_key("augment_context_for_speech")

    def get_augmentation_sigma(self) -> int:
        return self._get_config_key("augmentation_sigma")

    def get_default_voice_model(self) -> str:
        return self._get_config_key("default_voice_model")

    def get_time_advanced_due_to_dialogue(self) -> int:
        return self._get_config_key("time_advanced_due_to_dialogue")

    def get_time_advanced_due_to_exiting_location(self) -> int:
        return self._get_config_key("time_advanced_due_to_exiting_location")

    def get_time_advanced_due_to_traveling(self) -> int:
        return self._get_config_key("time_advanced_due_to_traveling")

    def get_time_advanced_due_to_searching_for_location(self) -> int:
        return self._get_config_key("time_advanced_due_to_searching_for_location")

    def get_max_retries(self) -> int:
        return self._get_config_key("max_retries")

    def get_narrator_voice_model(self) -> str:
        return self._get_config_key("narrator_voice_model")

    def get_default_weather_icon(self) -> str:
        return self._get_config_key("default_weather_icon")

    def get_facts_to_retrieve_from_database(self) -> int:
        return self._get_config_key("facts_to_retrieve_from_database")

    def get_memories_to_retrieve_from_database(self) -> int:
        return self._get_config_key("memories_to_retrieve_from_database")

    def get_number_of_characters_to_retrieve_from_transcription(self) -> int:
        return self._get_config_key(
            "number_of_characters_to_retrieve_from_transcription"
        )

    def get_number_of_characters_to_retrieve_from_interview(self) -> int:
        return self._get_config_key("number_of_characters_to_retrieve_from_interview")

    def load_openai_project_key(self) -> str:
        return self._load_secret_key(self._path_manager.get_openai_project_key_path())

    def load_openai_secret_key(self) -> str:
        return self._load_secret_key(self._path_manager.get_openai_secret_key_path())

    def load_openrouter_secret_key(self) -> str:
        return self._load_secret_key(
            self._path_manager.get_openrouter_secret_key_path()
        )

    def load_runpod_secret_key(self) -> str:
        return self._load_secret_key(self._path_manager.get_runpod_secret_key_path())
