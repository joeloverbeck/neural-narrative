from typing import Protocol

from src.enums import AiCompletionErrorType


class AiCompletionProduct(Protocol):
    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> AiCompletionErrorType:
        pass