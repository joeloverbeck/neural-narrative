from typing import Optional

from src.base.required_string import RequiredString


class ConnectionProduct:
    def __init__(
            self,
            connection: Optional[RequiredString],
            is_valid: bool,
            error: Optional[str] = None,
    ):
        self._connection = connection
        self._is_valid = is_valid
        self._error = error

    def get(self) -> RequiredString:
        return self._connection

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
