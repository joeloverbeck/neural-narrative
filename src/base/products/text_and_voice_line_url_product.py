from pathlib import Path
from typing import Optional


class TextAndVoiceLineUrlProduct:

    def __init__(self, text: str, voice_line_url: Optional[Path]):
        self._text = text
        self._voice_line_url = voice_line_url

    def get_text(self) -> str:
        return self._text

    def get_voice_line_file_name(self) -> Path:
        return self._voice_line_url
