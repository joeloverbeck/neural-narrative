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
        self._character_name = character_name
        self._voice_model = voice_model
        self._temp_dir = temp_dir
        self._temp_file_paths = temp_file_paths
        self._voice_manager = voice_manager or VoiceManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def provide_file_name(self) -> Optional[str]:
        file_name = self._filesystem_manager.get_file_path_for_voice_line(
            self._character_name, self._voice_model
        )
        if len(self._temp_file_paths) > 1:
            try:
                self._voice_manager.concatenate_wav_files_from_list(
                    self._temp_file_paths, file_name
                )
            except Exception as e:
                logger.error(f"Error concatenating voice lines: {e}")
                return None
        elif len(self._temp_file_paths) == 1:
            temp_file = self._temp_file_paths[0]
            try:
                self._filesystem_manager.copy_file(temp_file, file_name)
                logger.info(f"Copied single temp file {temp_file} to {file_name}")
            except Exception as e:
                logger.error(f"Error copying file {temp_file} to {file_name}: {e}")
                return None
        else:
            logger.error("No temporary files to process.")
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
        if not isinstance(file_name, str):
            raise TypeError(
                f"This function should return a str, which would be the file name of the created line, but it was '{type(file_name)}'."
            )
        return file_name
