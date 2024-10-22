from typing import Optional


class SelfReflectionProduct:

    def __init__(self, self_reflection: str, is_valid: bool, error:
    Optional[str] = None):
        self._self_reflection = self_reflection
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._self_reflection

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
