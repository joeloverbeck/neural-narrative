from typing import Optional


class DictProduct:
    def __init__(self, data: dict, is_valid: bool, error: Optional[str] = None):
        self._data = data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
