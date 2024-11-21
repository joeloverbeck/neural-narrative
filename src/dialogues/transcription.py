from typing import List, Optional

from src.filesystem.config_loader import ConfigLoader


class Transcription:

    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self._transcription: List[str] = []

        self._config_loader = config_loader or ConfigLoader()

    def add_speech_turn(self, name: str, speech: str):
        self._transcription.append(f"{name}: {speech}")

    def add_line(self, line: str):
        self._transcription.append(line)

    def get(self) -> List[str]:
        return self._transcription

    def get_prettified_transcription(self) -> str:
        prettified_dialogue = ""
        for speech_turn in self._transcription:
            prettified_dialogue += f"{speech_turn}\n"
        return prettified_dialogue + "\n"

    def get_transcription_excerpt(self) -> str:
        return self.get_prettified_transcription()[
            -self._config_loader.get_number_of_characters_to_retrieve_from_transcription() :
        ]

    def is_transcription_sufficient(self) -> bool:
        return self._transcription and len(self._transcription) > 4
