from src.services.voices_services import VoicesServices

if __name__ == "__main__":
    directory = "static/voice_lines"  # Replace with the path to your directory
    output_file = "test_convo.wav"  # Replace with your desired output file path

    VoicesServices().concatenate_wav_files(directory, output_file)
