import logging
from pathlib import Path
from typing import List, Optional

from src.base.exceptions import VoiceLineGenerationError
from src.filesystem.path_manager import PathManager
from src.requests.requests_manager import RequestsManager
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.voice_part_provider_factory import VoicePartProviderFactory

logger = logging.getLogger(__name__)


class ProduceVoicePartsAlgorithm:
    def __init__(
        self,
        text_parts: List[str],
        timestamp: str,
        voice_part_provider_factory: VoicePartProviderFactory,
        requests_manager: Optional[RequestsManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        self._text_parts = text_parts
        self._timestamp = timestamp
        self._voice_part_provider_factory = voice_part_provider_factory

        self._requests_manager = requests_manager or RequestsManager()
        self._path_manager = path_manager

    def do_algorithm(self) -> List[Path]:
        xtts_endpoint = self._requests_manager.get_xtts_endpoint()

        if not xtts_endpoint:
            return []

        temp_dir = self._path_manager.get_temp_voice_lines_path(self._timestamp)

        temp_file_paths = []

        for index, part in enumerate(self._text_parts):
            voice_part_provider_config = VoicePartProviderConfig(
                part, xtts_endpoint, self._timestamp, index, temp_dir, temp_file_paths
            )
            try:
                self._voice_part_provider_factory.create_provider(
                    voice_part_provider_config
                ).create_voice_part()
            except VoiceLineGenerationError as e:
                logger.error(
                    f"Failed to generate voice line for part '%s'. Error: %s", part, e
                )

        return temp_file_paths