from typing import Protocol


class UrlContentProduct(Protocol):
    def get(self) -> bytes:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
