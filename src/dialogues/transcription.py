from typing import List


class Transcription:

    def __init__(self):
        self._transcription: List[str] = []

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

    def is_transcription_sufficient(self) -> bool:
        return self._transcription and len(self._transcription) > 4
