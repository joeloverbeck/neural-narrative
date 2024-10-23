from pydantic import BaseModel

from src.prompting.abstracts.factory_products import LlmContentProduct


class BaseModelLlmContentProduct(LlmContentProduct):

    def __init__(self, content: BaseModel, is_valid: bool, error: str = None):
        self._content = content
        self._is_valid = is_valid
        self._error = error

    def get(self) -> BaseModel:
        return self._content

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
