from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.providers.voice_part_provider import VoicePartProvider


class VoicePartProviderFactory:
    def __init__(
        self,
        character_name: str,
        voice_model: str,
        generate_voice_line_algorithm_factory: GenerateVoiceLineAlgorithmFactory,
    ):
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        self._character_name = character_name
        self._voice_model = voice_model

        self._generate_voice_line_algorithm_factory = (
            generate_voice_line_algorithm_factory
        )

    def create_provider(
        self, voice_part_provider_config: VoicePartProviderConfig
    ) -> VoicePartProvider:
        return VoicePartProvider(
            self._character_name,
            self._voice_model,
            voice_part_provider_config,
            self._generate_voice_line_algorithm_factory,
        )
