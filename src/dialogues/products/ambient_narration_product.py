from typing import Optional

from src.base.required_string import RequiredString


class AmbientNarrationProduct:
    def __init__(
            self,
            ambient_narration: RequiredString,
            is_valid: bool,
            error: Optional[str] = None,
    ):
        self._ambient_narration = ambient_narration
        self._is_valid = is_valid
        self._error = error

    def get(self) -> RequiredString:
        return self._ambient_narration

    def get_error(self) -> str:
        return self._error

    def is_valid(self) -> bool:
        return self._is_valid
