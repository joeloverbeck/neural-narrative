from typing import Protocol, Union

from pydantic import BaseModel

from src.base.enums import AiCompletionErrorType


class AiCompletionProduct(Protocol):

    def get(self) -> Union[str, BaseModel]:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> AiCompletionErrorType:
        pass

    def get_error_details(self) -> str:
        pass
