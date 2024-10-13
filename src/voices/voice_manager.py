import logging
import os
import wave
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from src.constants import VOICE_MODELS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.requests.requests_manager import RequestsManager
from src.voices.algorithms.generate_voice_line_algorithm import (
    GenerateVoiceLineAlgorithm,
)
from src.voices.factories.voice_line_factory import VoiceLineFactory

logger = logging.getLogger(__name__)


class VoiceManager:
    def __init__(
        self,
        requests_manager: Optional[RequestsManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._requests_manager = requests_manager or RequestsManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        self._executor = ThreadPoolExecutor(max_workers=4)

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

    def concatenate_wav_files(self, directory, output_file, silence_duration=1.0):
        """
        Concatenate all .wav files in the directory into a single .wav file.
        Files are sorted based on the timestamp extracted from their filenames.
        Adds silence between files.

        Args:
            directory (str): Path to the directory containing .wav files.
            output_file (str): Path to save the output concatenated file.
            silence_duration (float): Duration of silence (in seconds) between each file.
        """
        # Get a list of all .wav files in the directory
        wav_files = [f for f in os.listdir(directory) if f.endswith(".wav")]

        # Sort the files based on their timestamps
        wav_files_sorted = sorted(wav_files, key=self._get_timestamp)

        # Initialize variables
        data = []
        params = None
        silence_frames = None  # Will hold the silent frames

        # Read frames from each .wav file
        for wav_file in wav_files_sorted:
            wav_path = os.path.join(directory, wav_file)
            with wave.open(wav_path, "rb") as w:
                current_params = w.getparams()

                # Print current parameters for debugging
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
                            f"Audio parameters of {wav_file} do not match the initial parameters."
                        )

                frames = w.readframes(w.getnframes())
                data.append(frames)
                data.append(silence_frames)  # Add silence after each file

        # Write the concatenated frames to the output file
        with wave.open(output_file, "wb") as out_wav:
            out_wav.setparams(params)  # Use the first file's parameters
            for frames in data:
                out_wav.writeframes(frames)
            logger.info(f"Successfully created '%s'.", output_file)

    def generate_voice_line(
        self, character_name: str, text: str, voice_model: str
    ) -> Optional[str]:
        if not character_name:
            raise ValueError("character_name can't be empty.")
        if not text:
            raise ValueError("text can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

        xtts_endpoint = RequestsManager().get_xtts_endpoint()

        if xtts_endpoint:
            # Produce a voice line.
            voice_line_factory = VoiceLineFactory(text, voice_model, xtts_endpoint)

            file_name, file_path = (
                self._filesystem_manager.get_file_path_for_voice_line(
                    character_name, voice_model
                )
            )

            algorithm = GenerateVoiceLineAlgorithm(file_path, voice_line_factory)

            # Submit the generation to a separate thread
            future = self._executor.submit(algorithm.generate_voice_line)

            # Optionally, handle the future (e.g., logging success/failure)
            def handle_result(fut):
                try:
                    fut.result()  # Will raise if there was an exception
                    logger.info(
                        f"Voice line generated successfully for {character_name}."
                    )
                except Exception as e:
                    logger.error(
                        f"Error generating voice line for {character_name}: {e}"
                    )

            future.add_done_callback(handle_result)

            return file_name
        else:
            logger.warning(
                "Not running a RunPod pod, which is necessary to create voice lines."
            )

        return None
