import os
from datetime import datetime

from src.base.required_string import RequiredString
from src.voices.voice_manager import VoiceManager


def get_timestamp(filename):
    """
    Extract the timestamp from the filename.
    Assumes the timestamp is the first 14 characters of the filename.
    """
    return filename[:14]


if __name__ == "__main__":
    output_file = RequiredString(
        f"{datetime.now().strftime("%Y%m%d%H%M%S")}.wav"
    )  # Replace with your desired output file path

    directory = "static/voice_lines_to_join"  # Replace with the path to your directory

    # Get a list of all .wav files in the directory
    wav_files = [f for f in os.listdir(directory) if f.endswith(".wav")]

    # Sort the files based on their timestamps
    wav_files_sorted = sorted(wav_files, key=get_timestamp)

    final_wav_files = [
        RequiredString(os.path.join(directory, file_name))
        for file_name in wav_files_sorted
    ]

    VoiceManager.concatenate_wav_files_from_list(final_wav_files, output_file)
