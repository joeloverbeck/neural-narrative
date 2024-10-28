import logging
import wave
from pathlib import Path
from typing import Optional, List

from src.filesystem.file_operations import read_json_file, create_directories
from src.filesystem.path_manager import PathManager
from src.requests.requests_manager import RequestsManager

logger = logging.getLogger(__name__)


class VoiceManager:

    def __init__(
        self,
        requests_manager: Optional[RequestsManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        self._requests_manager = requests_manager or RequestsManager()
        self._path_manager = path_manager or PathManager()

        create_directories(self._path_manager.VOICE_LINES_DIR)

    def get_all_tags(self):
        all_tags = set()
        for tags in read_json_file(self._path_manager.get_voice_models_path()).values():
            all_tags.update(tags)
        return sorted(all_tags)

    def filter_voice_models_by_tags(self, selected_tags):
        filtered_voice_models = {
            vm_name: tags
            for vm_name, tags in read_json_file(
                self._path_manager.get_voice_models_path()
            ).items()
            if all(tag in tags for tag in selected_tags)
        }
        return filtered_voice_models

    @staticmethod
    def concatenate_wav_files_from_list(
        file_paths: List[Path], output_file: Path, silence_duration=1.0
    ):
        """
        Concatenate the list of .wav files into a single .wav file.
        Adds silence between files.

        Args:
            file_paths (list of Path): List of paths to .wav files to concatenate.
            output_file (Path): Path to save the output concatenated file.
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
            path = wav_path.as_posix() if isinstance(wav_path, Path) else wav_path
            with wave.open(path, "rb") as w:
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

        path = output_file.as_posix() if isinstance(output_file, Path) else output_file

        with wave.open(path, "wb") as out_wav:
            out_wav.setparams(params)
            for frames in data:
                out_wav.writeframes(frames)
            logger.info(f"Successfully created '%s'.", output_file)
