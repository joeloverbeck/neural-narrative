from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager
from src.requests.requests_manager import RequestsManager
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


def main():
    available_speakers = RequestsManager().get_available_speakers()
    implemented_voice_models = read_json_file(PathManager().get_voice_models_path())
    implemented_models_set = set(implemented_voice_models.keys())
    unimplemented_speakers = [
        speaker
        for speaker in available_speakers
        if speaker not in implemented_models_set
    ]
    text_to_read = "I'm absolutely thrilled to share this wonderful news with you! It's hard to believe that our journey has come to an end. Quickly, we need to secure the perimeter before nightfall! In the stillness of the night, every sound echoes louder than the last. The quantum processor operates at unprecedented speeds, revolutionizing computational capabilities. Once upon a time, in a land far away, there lived a brave young explorer. Would you care for a spot of tea while we discuss the matter?"
    for available_speaker in unimplemented_speakers:
        file_path = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            "test", text_to_read, available_speaker
        ).direct_voice_line_generation()
        print(f"Generated voice line for '{file_path}'")


if __name__ == "__main__":
    main()
