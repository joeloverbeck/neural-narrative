from typing import Optional

from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConcreteLlmToolResponseProduct(LlmToolResponseProduct):
    def __init__(self, llm_response: dict, is_valid: bool, error: Optional[str] = None):
        self._llm_response = llm_response
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._llm_response

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
