from typing import Optional


class CharacterDescriptionProduct:
    def __init__(self, description: str, is_valid: bool, error: Optional[str] = None):
        if not description:
            raise ValueError("description can't be empty.")

        self._description = description
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._description

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
