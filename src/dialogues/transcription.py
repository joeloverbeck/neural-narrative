from typing import List

from src.base.required_string import RequiredString


class Transcription:
    def __init__(self):
        self._transcription: List[RequiredString] = []

    def add_speech_turn(self, name: RequiredString, speech: RequiredString):
        self._transcription.append(RequiredString(f"{name}: {speech}"))

    def add_line(self, line: RequiredString):
        self._transcription.append(line)

    def get(self) -> List[RequiredString]:
        return self._transcription

    def get_prettified_transcription(self) -> RequiredString:
        prettified_dialogue = ""

        for speech_turn in self._transcription:
            prettified_dialogue += f"{speech_turn}\n"

        return prettified_dialogue + "\n"

    def is_transcription_sufficient(self) -> bool:
        return self._transcription and len(self._transcription) > 4
