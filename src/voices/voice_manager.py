import logging
import wave
from typing import Optional, List

from src.base.constants import VOICE_MODELS_FILE
from src.base.required_string import RequiredString
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
    def _get_timestamp(filename):
        """
        Extract the timestamp from the filename.
        Assumes the timestamp is the first 14 characters of the filename.
        """
        return filename[:14]

    def get_all_tags(self):
        # Get a set of all tags from all voice models
        all_tags = set()
        for tags in self._filesystem_manager.load_existing_or_new_json_file(
            VOICE_MODELS_FILE
        ).values():
            all_tags.update(tags)
        return sorted(all_tags)

    def filter_voice_models_by_tags(self, selected_tags):
        # Filter voice models that have all the selected tags
        filtered_voice_models = {
            vm_name: tags
            for vm_name, tags in self._filesystem_manager.load_existing_or_new_json_file(
                VOICE_MODELS_FILE
            ).items()
            if all(tag in tags for tag in selected_tags)
        }

        return filtered_voice_models

    @staticmethod
    def concatenate_wav_files_from_list(
        file_paths: List[RequiredString],
        output_file: RequiredString,
        silence_duration=1.0,
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
            with wave.open(wav_path.value, "rb") as w:
                current_params = w.getparams()

                # Initialize parameters with the first file's settings
                if params is None:
                    params = current_params
                    # Calculate silent frames for the given silence duration
                    silence_frames = b"\x00" * int(
                        params.framerate
                        * silence_duration
                        * params.nchannels
                        * params.sampwidth
                    )
                else:
                    # Check only the relevant parameters (ignore nframes)
                    if (
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
                data.append(silence_frames)  # Add silence after each file

        # Write the concatenated frames to the output file
        with wave.open(output_file.value, "wb") as out_wav:
            out_wav.setparams(params)  # Use the first file's parameters
            for frames in data:
                out_wav.writeframes(frames)
            logger.info(f"Successfully created '%s'.", output_file)

    def generate_voice_line(
        self, character_name: str, text: str, voice_model: str
    ) -> Optional[str]:
        pass
