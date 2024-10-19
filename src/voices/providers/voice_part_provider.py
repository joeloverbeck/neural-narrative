import logging
import os

from src.base.constants import NARRATOR_VOICE_MODEL
from src.base.exceptions import VoiceLineGenerationError
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class VoicePartProvider:

    def __init__(
        self,
        character_name: str,
        voice_model: str,
        voice_part_provider_config: VoicePartProviderConfig,
        generate_voice_line_algorithm_factory: GenerateVoiceLineAlgorithmFactory,
    ):
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        self._character_name = character_name
        self._voice_model = voice_model
        self._voice_part_provider_config = voice_part_provider_config
        self._generate_voice_line_algorithm_factory = (
            generate_voice_line_algorithm_factory
        )

    def create_voice_part(self) -> None:
        clean_text = self._voice_part_provider_config.part.strip()
        if not clean_text:
            return

        if clean_text.startswith("*") and clean_text.endswith("*"):
            voice_to_use = NARRATOR_VOICE_MODEL
            clean_text = clean_text.strip("*").strip()
        else:
            voice_to_use = self._voice_model

        if not clean_text:
            # Skip parts that become empty after stripping
            return

        temp_file_name = f"{self._voice_part_provider_config.timestamp}_{self._character_name}_{voice_to_use}_{self._voice_part_provider_config.index}.wav"
        temp_file_path = os.path.join(
            self._voice_part_provider_config.temp_dir, temp_file_name
        )

        algorithm = self._generate_voice_line_algorithm_factory.create_algorithm(
            clean_text,
            voice_to_use,
            self._voice_part_provider_config.xtts_endpoint,
            temp_file_path,
        )

        # Generate voice line synchronously
        try:
            algorithm.generate_voice_line()
            self._voice_part_provider_config.temp_file_paths.append(temp_file_path)
        except Exception as e:
            raise VoiceLineGenerationError(
                f"Error generating voice line for part {self._voice_part_provider_config.index}: {e}"
            ) from e
