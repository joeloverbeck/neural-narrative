from datetime import datetime

from src.voices.voice_manager import VoiceManager

if __name__ == "__main__":
    directory = "static/voice_lines_to_join"  # Replace with the path to your directory
    output_file = f"{datetime.now().strftime("%Y%m%d%H%M%S")}.wav"  # Replace with your desired output file path

    VoiceManager().concatenate_wav_files(directory, output_file)
