import logging
import re
import time
from typing import Optional

from src.exceptions import VoiceLineGenerationError
from src.filesystem.filesystem_manager import FilesystemManager
from src.requests.requests_manager import RequestsManager
from src.voices.configs.voice_part_provider_config import VoicePartProviderConfig
from src.voices.factories.voice_line_file_name_provider_factory import (
    VoiceLineFileNameProviderFactory,
)
from src.voices.factories.voice_part_provider_factory import VoicePartProviderFactory

logger = logging.getLogger(__name__)


class DirectVoiceLineGenerationAlgorithm:
    def __init__(
        self,
        text: str,
        voice_part_provider_factory: VoicePartProviderFactory,
        voice_line_file_name_provider_factory: VoiceLineFileNameProviderFactory,
        requests_manager: Optional[RequestsManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not text:
            raise ValueError("text can't be empty.")

        self._text = text
        self._voice_part_provider_factory = voice_part_provider_factory
        self._voice_line_file_name_provider_factory = (
            voice_line_file_name_provider_factory
        )

        self._requests_manager = requests_manager or RequestsManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def direct_voice_line_generation(self) -> Optional[str]:
        xtts_endpoint = self._requests_manager.get_xtts_endpoint()

        if not xtts_endpoint:
            logger.warning(
                "Not running a RunPod pod, which is necessary to create voice lines."
            )
            return None

        # Split text into parts
        parts = re.split(r"(\*.*?\*)", self._text)

        parts = [part for part in parts if part]

        temp_file_paths = []
        timestamp = time.strftime("%Y%m%d%H%M%S")

        # Directory to store temporary files
        temp_dir = self._filesystem_manager.get_temporary_folder_to_store_voice_parts(
            timestamp
        )

        for index, part in enumerate(parts):
            voice_part_provider_config = VoicePartProviderConfig(
                part,
                xtts_endpoint,
                timestamp,
                index,
                temp_dir,
                temp_file_paths,
            )

            try:
                self._voice_part_provider_factory.create_provider(
                    voice_part_provider_config
                ).create_voice_part()
            except VoiceLineGenerationError as e:
                logger.error(
                    f"Failed to generate voice line for part '%s'. Error: %s", part, e
                )

        if temp_file_paths:
            return self._voice_line_file_name_provider_factory.create_factory(
                temp_dir, temp_file_paths
            ).provide_file_name()
        else:
            logger.warning("No voice lines were generated.")
            return None
