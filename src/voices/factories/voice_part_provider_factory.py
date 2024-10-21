from src.base.required_string import RequiredString
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.providers.voice_part_provider import VoicePartProvider


class VoicePartProviderFactory:
    def __init__(
        self,
        character_name: RequiredString,
        voice_model: RequiredString,
        generate_voice_line_algorithm_factory: GenerateVoiceLineAlgorithmFactory,
    ):
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
