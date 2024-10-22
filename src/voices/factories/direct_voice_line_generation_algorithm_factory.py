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
        voice_line_file_name_provider_factory = VoiceLineFileNameProviderFactory(
            character_name, voice_model
        )
        generate_voice_line_algorithm_factory = GenerateVoiceLineAlgorithmFactory()
        voice_part_provider_factory = VoicePartProviderFactory(
            character_name, voice_model, generate_voice_line_algorithm_factory
        )
        return DirectVoiceLineGenerationAlgorithm(
            text, voice_part_provider_factory, voice_line_file_name_provider_factory
        )
