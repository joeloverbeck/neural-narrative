from typing import Optional


class AmbientNarrationProduct:
    def __init__(
        self, ambient_narration: str, is_valid: bool, error: Optional[str] = None
    ):
        if not ambient_narration:
            raise ValueError("ambient_narration can't be empty.")

        self._ambient_narration = ambient_narration
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._ambient_narration

    def get_error(self) -> str:
        return self._error

    def is_valid(self) -> bool:
        return self._is_valid
