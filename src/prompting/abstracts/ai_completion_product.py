from typing import Protocol

from src.base.enums import AiCompletionErrorType


class AiCompletionProduct(Protocol):
    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> AiCompletionErrorType:
        pass

    def get_error_details(self) -> str:
        pass
