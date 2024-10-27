import logging
import re
import time
from typing import Optional

from src.base.validators import validate_non_empty_string
from src.filesystem.config_loader import ConfigLoader
from src.filesystem.file_operations import create_directories
from src.filesystem.path_manager import PathManager
from src.requests.requests_manager import RequestsManager
from src.voices.factories.produce_voice_parts_algorithm_factory import (
    ProduceVoicePartsAlgorithmFactory,
)
from src.voices.factories.voice_line_file_name_provider_factory import (
    VoiceLineFileNameProviderFactory,
)

logger = logging.getLogger(__name__)


class DirectVoiceLineGenerationAlgorithm:

    def __init__(
        self,
        text: str,
        produce_voice_parts_algorithm_factory: ProduceVoicePartsAlgorithmFactory,
        voice_line_file_name_provider_factory: VoiceLineFileNameProviderFactory,
        requests_manager: Optional[RequestsManager] = None,
        config_loader: Optional[ConfigLoader] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(text, "text")

        self._text = text
        self._produce_voice_parts_algorithm_factory = (
            produce_voice_parts_algorithm_factory
        )
        self._voice_line_file_name_provider_factory = (
            voice_line_file_name_provider_factory
        )

        self._requests_manager = requests_manager or RequestsManager()
        self._config_loader = config_loader or ConfigLoader()
        self._path_manager = path_manager or PathManager()

    def direct_voice_line_generation(self) -> Optional[str]:
        if not self._config_loader.get_produce_voice_lines():
            return None

        xtts_endpoint = self._requests_manager.get_xtts_endpoint()

        if not xtts_endpoint:
            logger.warning(
                "Not running a RunPod pod, which is necessary to create voice lines."
            )
            return None

        parts = re.split("(\\*.*?\\*)", self._text)
        parts = [part for part in parts if part]

        timestamp = time.strftime("%Y%m%d%H%M%S")

        temp_dir = self._path_manager.get_temp_voice_lines_path(timestamp)

        # Ensure folder for temporary voice lines exists.
        create_directories(temp_dir)

        temp_file_paths = self._produce_voice_parts_algorithm_factory.create_algorithm(
            parts, timestamp
        ).do_algorithm()

        if temp_file_paths:
            return self._voice_line_file_name_provider_factory.create_factory(
                temp_dir, temp_file_paths
            ).provide_file_name()
        else:
            logger.warning("No voice lines were generated.")
            return None
