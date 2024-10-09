from typing import Optional


class MatchingVoiceModelProduct:

    def __init__(
        self, voice_model: Optional[str], is_valid: bool, error: Optional[str] = None
    ):
        self._voice_model = voice_model
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._voice_model

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
