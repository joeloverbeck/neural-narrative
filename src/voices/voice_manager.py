import logging
import wave
from pathlib import Path
from typing import Optional, List

from src.base.constants import VOICE_MODELS_FILE
from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.requests.requests_manager import RequestsManager

logger = logging.getLogger(__name__)


class VoiceManager:

    def __init__(
        self,
        requests_manager: Optional[RequestsManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._requests_manager = requests_manager or RequestsManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    @staticmethod
    def get_all_tags():
        all_tags = set()
        for tags in read_json_file(Path(VOICE_MODELS_FILE)).values():
            all_tags.update(tags)
        return sorted(all_tags)

    @staticmethod
    def filter_voice_models_by_tags(selected_tags):
        filtered_voice_models = {
            vm_name: tags
            for vm_name, tags in read_json_file(Path(VOICE_MODELS_FILE)).items()
            if all(tag in tags for tag in selected_tags)
        }
        return filtered_voice_models

    @staticmethod
    def concatenate_wav_files_from_list(
        file_paths: List[str], output_file: str, silence_duration=1.0
    ):
        """
        Concatenate the list of .wav files into a single .wav file.
        Adds silence between files.

        Args:
            file_paths (list of str): List of paths to .wav files to concatenate.
            output_file (str): Path to save the output concatenated file.
            silence_duration (float): Duration of silence (in seconds) between each file.
        """
        if len(file_paths) <= 1:
            logger.info(
                f"Attempted to concatenate voice lines where there weren't at least two: {file_paths}"
            )
            return
        data = []
        params = None
        silence_frames = None
        for wav_path in file_paths:
            with wave.open(wav_path, "rb") as w:
                current_params = w.getparams()
                if params is None:
                    params = current_params
                    silence_frames = b"\x00" * int(
                        params.framerate
                        * silence_duration
                        * params.nchannels
                        * params.sampwidth
                    )
                elif (
                    current_params.nchannels != params.nchannels
                    or current_params.sampwidth != params.sampwidth
                    or current_params.framerate != params.framerate
                    or current_params.comptype != params.comptype
                ):
                    raise ValueError(
                        f"Audio parameters of {wav_path} do not match the initial parameters."
                    )
                frames = w.readframes(w.getnframes())
                data.append(frames)
                data.append(silence_frames)
        with wave.open(output_file, "wb") as out_wav:
            out_wav.setparams(params)
            for frames in data:
                out_wav.writeframes(frames)
            logger.info(f"Successfully created '%s'.", output_file)

    def generate_voice_line(
        self, character_name: str, text: str, voice_model: str
    ) -> Optional[str]:
        pass
