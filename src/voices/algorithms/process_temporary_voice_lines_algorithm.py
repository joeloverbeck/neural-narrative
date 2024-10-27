import logging
from pathlib import Path
from typing import List, Optional

from src.filesystem.file_operations import copy_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.products.process_temporary_voice_lines_algorithm_product import (
    ProcessTemporaryVoiceLinesAlgorithmProduct,
)
from src.voices.voice_manager import VoiceManager

logger = logging.getLogger(__name__)


class ProcessTemporaryVoiceLinesAlgorithm:
    def __init__(
        self,
        temp_file_paths: List[Path],
        file_name: Path,
        voice_manager: Optional[VoiceManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._temp_file_paths = temp_file_paths
        self._file_name = file_name

        self._voice_manager = voice_manager or VoiceManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def do_algorithm(self) -> ProcessTemporaryVoiceLinesAlgorithmProduct:
        if len(self._temp_file_paths) > 1:
            try:
                self._voice_manager.concatenate_wav_files_from_list(
                    self._temp_file_paths, self._file_name
                )
            except Exception as e:
                logger.error(f"Error concatenating voice lines: {e}")
                return ProcessTemporaryVoiceLinesAlgorithmProduct(success=False)
        elif len(self._temp_file_paths) == 1:
            temp_file = self._temp_file_paths[0]
            try:
                copy_file(temp_file, self._file_name)
                logger.info(f"Copied single temp file {temp_file} to {self._file_name}")
            except Exception as e:
                logger.error(
                    f"Error copying file {temp_file} to {self._file_name}: {e}"
                )
                return ProcessTemporaryVoiceLinesAlgorithmProduct(success=False)
        else:
            logger.error("No temporary files to process.")
            return ProcessTemporaryVoiceLinesAlgorithmProduct(success=False)

        return ProcessTemporaryVoiceLinesAlgorithmProduct(success=True)
