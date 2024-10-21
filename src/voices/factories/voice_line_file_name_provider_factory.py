from typing import List

from src.base.required_string import RequiredString
from src.voices.providers.voice_line_file_name_provider import VoiceLineFileNameProvider


class VoiceLineFileNameProviderFactory:
    def __init__(self, character_name: RequiredString, voice_model: RequiredString):
        self._character_name = character_name
        self._voice_model = voice_model

    def create_factory(
        self, temp_dir: RequiredString, temp_file_paths: List[RequiredString]
    ) -> VoiceLineFileNameProvider:
        return VoiceLineFileNameProvider(
            self._character_name, self._voice_model, temp_dir, temp_file_paths
        )
