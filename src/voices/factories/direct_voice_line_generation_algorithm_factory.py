from src.voices.algorithms.direct_voice_line_generation_algorithm import (
    DirectVoiceLineGenerationAlgorithm,
)
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.factories.voice_line_file_name_provider_factory import (
    VoiceLineFileNameProviderFactory,
)
from src.voices.factories.voice_part_provider_factory import VoicePartProviderFactory


class DirectVoiceLineGenerationAlgorithmFactory:

    @staticmethod
    def create_algorithm(
        character_name: str, text: str, voice_model: str
    ) -> DirectVoiceLineGenerationAlgorithm:
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not text:
            raise ValueError("text can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        voice_line_file_name_provider_factory = VoiceLineFileNameProviderFactory(
            character_name, voice_model
        )

        generate_voice_line_algorithm_factory = GenerateVoiceLineAlgorithmFactory()

        voice_part_provider_factory = VoicePartProviderFactory(
            character_name, voice_model, generate_voice_line_algorithm_factory
        )

        return DirectVoiceLineGenerationAlgorithm(
            text,
            voice_part_provider_factory,
            voice_line_file_name_provider_factory,
        )
