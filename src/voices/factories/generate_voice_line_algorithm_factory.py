from pathlib import Path

from src.voices.algorithms.generate_voice_line_algorithm import (
    GenerateVoiceLineAlgorithm,
)
from src.voices.factories.voice_line_factory import VoiceLineFactory


class GenerateVoiceLineAlgorithmFactory:

    @staticmethod
    def create_algorithm(
        text: str, voice_model: str, xtts_endpoint: str, file_path: Path
    ) -> GenerateVoiceLineAlgorithm:
        if not text:
            raise ValueError("text can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")
        if not xtts_endpoint:
            raise ValueError("xtts_endpoint can't be empty.")
        voice_line_factory = VoiceLineFactory(text, voice_model, xtts_endpoint)
        return GenerateVoiceLineAlgorithm(file_path, voice_line_factory)
