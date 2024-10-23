from pydantic import BaseModel

from src.base.enums import AiCompletionErrorType
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct


class InstructorAiCompletionProduct(AiCompletionProduct):
    def __init__(self, completion_result: BaseModel):
        self._completion_result = completion_result

    def get(self) -> str:
        raise NotImplemented("Not implemented")

    def is_valid(self) -> bool:
        raise NotImplemented("Not implemented")

    def get_error(self) -> AiCompletionErrorType:
        raise NotImplemented("Not implemented")

    def get_error_details(self) -> str:
        raise NotImplemented("Not implemented")
