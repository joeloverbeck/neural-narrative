from typing import Protocol

from src.base.required_string import RequiredString


class GeneratedImageProduct(Protocol):
    def get(self) -> RequiredString:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
