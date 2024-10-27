from typing import Optional


class TextProduct:

    def __init__(self, text: str, is_valid: bool, error: Optional[str] = None):
        self._text = text
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._text

    def get_error(self) -> str:
        return self._error

    def is_valid(self) -> bool:
        return self._is_valid
