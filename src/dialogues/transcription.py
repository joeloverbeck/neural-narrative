from typing import List


class Transcription:
    def __init__(self):
        self._transcription: List[str] = []

    def add_speech_turn(self, name: str, speech: str):
        if not name:
            raise ValueError("name should not be empty.")
        if not speech:
            raise ValueError("speech should not be empty.")

        self._transcription.append(f"{name}: {speech}")

    def get(self) -> List[str]:
        return self._transcription

    def is_transcription_sufficient(self) -> bool:
        return self._transcription and len(self._transcription) > 4