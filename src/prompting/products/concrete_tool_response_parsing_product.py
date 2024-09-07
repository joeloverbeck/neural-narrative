from typing import Optional

from src.prompting.abstracts.factory_products import ToolResponseParsingProduct


class ConcreteToolResponseParsingProduct(ToolResponseParsingProduct):
    def __init__(self, function_json: Optional[dict], is_valid: bool, error: Optional[str]):
        self._function_json = function_json
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._function_json

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
