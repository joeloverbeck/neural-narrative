from typing import Optional


class SecretsProduct:
    def __init__(self, secrets: str, is_valid: bool, error: Optional[str] = None):
        self._secrets = secrets
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._secrets

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
