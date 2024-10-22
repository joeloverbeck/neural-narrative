import os
from datetime import datetime

from src.voices.voice_manager import VoiceManager


def get_timestamp(filename):
    """
    Extract the timestamp from the filename.
    Assumes the timestamp is the first 14 characters of the filename.
    """
    return filename[:14]


if __name__ == "__main__":
    output_file = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    directory = "static/voice_lines_to_join"
    wav_files = [f for f in os.listdir(directory) if f.endswith(".wav")]
    wav_files_sorted = sorted(wav_files, key=get_timestamp)
    final_wav_files = [
        os.path.join(directory, file_name) for file_name in wav_files_sorted
    ]
    VoiceManager.concatenate_wav_files_from_list(final_wav_files, output_file)
