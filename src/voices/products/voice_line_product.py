from io import BytesIO
from typing import Optional


class VoiceLineProduct:

    def __init__(
        self,
        voice_line_data: Optional[BytesIO],
        is_valid: bool,
        error: Optional[str] = None,
    ):
        self._voice_line_data = voice_line_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> BytesIO:
        return self._voice_line_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
