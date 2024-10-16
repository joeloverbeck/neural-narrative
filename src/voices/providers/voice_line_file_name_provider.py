import logging
import os
from typing import Optional, List

from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.voice_manager import VoiceManager

logger = logging.getLogger(__name__)


class VoiceLineFileNameProvider:
    def __init__(
        self,
        character_name: str,
        voice_model: str,
        temp_dir: str,
        temp_file_paths: List[str],
        voice_manager: Optional[VoiceManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")
        if not temp_dir:
            raise ValueError("temp_dir can't be empty.")
        if not temp_file_paths:
            raise ValueError("temp_file_paths can't be empty.")

        self._character_name = character_name
        self._voice_model = voice_model
        self._temp_dir = temp_dir
        self._temp_file_paths = temp_file_paths

        self._voice_manager = voice_manager or VoiceManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def provide_file_name(self) -> Optional[str]:
        # Generate final file name and path
        file_name = self._filesystem_manager.get_file_path_for_voice_line(
            self._character_name, self._voice_model
        )

        # Concatenate the wav files
        try:
            self._voice_manager.concatenate_wav_files_from_list(
                self._temp_file_paths, file_name
            )
        except Exception as e:
            logger.error(f"Error concatenating voice lines: {e}")
            return None

        # Remove temporary files
        for temp_file in self._temp_file_paths:
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Error removing temporary file {temp_file}: {e}")

        # Remove temporary directory
        try:
            os.rmdir(self._temp_dir)
        except OSError as e:
            logger.warning(f"Error removing temporary directory {self._temp_dir}: {e}")

        return file_name
