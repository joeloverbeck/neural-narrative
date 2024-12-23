from src.prompting.abstracts.factory_products import LlmContentProduct


class UnparsedLlmContentProduct(LlmContentProduct):

    def __init__(self, content: str, is_valid: bool, error: str = None):
        self._content = content
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._content

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
