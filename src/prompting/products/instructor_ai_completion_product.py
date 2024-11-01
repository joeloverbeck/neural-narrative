from typing import Optional

from pydantic import BaseModel

from src.base.enums import AiCompletionErrorType
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct


class InstructorAiCompletionProduct(AiCompletionProduct):
    def __init__(
        self,
        completion_result: Optional[BaseModel],
        is_valid: bool,
        error: Optional[AiCompletionErrorType] = None,
    ):
        self._completion_result = completion_result
        self._is_valid = is_valid
        self._error: Optional[AiCompletionErrorType] = None

    def get(self) -> BaseModel:
        return self._completion_result

    def is_valid(self) -> bool:
        return self._completion_result is not None

    def get_error(self) -> Optional[AiCompletionErrorType]:
        return self._error

    def get_error_details(self) -> str:
        return str(self._completion_result) if self._error else ""
