from typing import Protocol


class GeneratedImageProduct(Protocol):
    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
