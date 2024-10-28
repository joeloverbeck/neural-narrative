import logging
from pathlib import Path
from typing import Optional

from src.base.exceptions import VoiceLineGenerationError
from src.base.tools import capture_traceback
from src.filesystem.config_loader import ConfigLoader
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
        config_loader: Optional[ConfigLoader] = None,
    ):
        self._character_name = character_name
        self._voice_model = voice_model
        self._voice_part_provider_config = voice_part_provider_config
        self._generate_voice_line_algorithm_factory = (
            generate_voice_line_algorithm_factory
        )

        self._config_loader = config_loader or ConfigLoader()

    def create_voice_part(self) -> Optional[Path]:
        clean_text = self._voice_part_provider_config.part.strip()
        if not clean_text:
            return None
        if clean_text.startswith("*") and clean_text.endswith("*"):
            voice_to_use = self._config_loader.get_narrator_voice_model()
            clean_text = clean_text.strip("*").strip()
        else:
            voice_to_use = self._voice_model
        if not clean_text:
            return None
        temp_file_name = Path(
            f"{self._voice_part_provider_config.timestamp}_{self._character_name}_{voice_to_use}_{self._voice_part_provider_config.index}.wav"
        )

        temp_file_path = self._voice_part_provider_config.temp_dir / temp_file_name

        algorithm = self._generate_voice_line_algorithm_factory.create_algorithm(
            clean_text,
            voice_to_use,
            self._voice_part_provider_config.xtts_endpoint,
            temp_file_path,
        )
        try:
            algorithm.generate_voice_line()
            return Path(temp_file_path)
        except Exception as e:
            capture_traceback()
            raise VoiceLineGenerationError(
                f"Error generating voice line for part {self._voice_part_provider_config.index}: {e}"
            ) from e
