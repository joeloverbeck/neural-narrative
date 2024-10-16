from typing import List

from src.voices.providers.voice_line_file_name_provider import VoiceLineFileNameProvider


class VoiceLineFileNameProviderFactory:
    def __init__(self, character_name: str, voice_model: str):
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        self._character_name = character_name
        self._voice_model = voice_model

    def create_factory(
        self, temp_dir: str, temp_file_paths: List[str]
    ) -> VoiceLineFileNameProvider:
        return VoiceLineFileNameProvider(
            self._character_name, self._voice_model, temp_dir, temp_file_paths
        )
