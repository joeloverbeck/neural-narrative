import logging
import os
from pathlib import Path
from typing import Optional, List

from src.base.validators import validate_non_empty_string
from src.filesystem.path_manager import PathManager
from src.voices.factories.process_temporary_voice_lines_algorithm_factory import (
    ProcessTemporaryVoiceLinesAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class VoiceLineFileNameProvider:

    def __init__(
        self,
        character_name: str,
        voice_model: str,
            temp_dir: Path,
            temp_file_paths: List[Path],
            process_temporary_voice_lines_algorithm_factory: ProcessTemporaryVoiceLinesAlgorithmFactory,
            path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(character_name, "character_name")
        validate_non_empty_string(voice_model, "voice_model")

        self._character_name = character_name
        self._voice_model = voice_model
        self._temp_dir = temp_dir
        self._temp_file_paths = temp_file_paths
        self._process_temporary_voice_lines_algorithm_factory = (
            process_temporary_voice_lines_algorithm_factory
        )

        self._path_manager = path_manager or PathManager()

    def provide_file_name(self) -> Optional[Path]:
        file_name = self._path_manager.get_voice_line_path(
            self._character_name, self._voice_model
        )

        product = (
            self._process_temporary_voice_lines_algorithm_factory.create_algorithm(
                file_name
            ).do_algorithm()
        )

        if not product.success:
            return None

        for temp_file in self._temp_file_paths:
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Error removing temporary file {temp_file}: {e}")

        try:
            os.rmdir(self._temp_dir)
        except OSError as e:
            logger.warning(f"Error removing temporary directory {self._temp_dir}: {e}")

        if not isinstance(file_name, Path):
            raise TypeError(
                f"This function should return a str, which would be the file name of the created line, but it was '{type(file_name)}'."
            )

        return file_name
