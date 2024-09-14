from typing import Optional

from src.requests.abstracts.factory_products import UrlContentProduct


class ConcreteUrlContentProduct(UrlContentProduct):
    def __init__(self, content: Optional[bytes], is_valid: bool, error: str = None):
        self._content = content
        self._is_valid = is_valid
        self._error = error

    def get(self) -> bytes:
        return self._content

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
