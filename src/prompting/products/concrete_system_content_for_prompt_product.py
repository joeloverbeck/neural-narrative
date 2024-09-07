from typing import Optional

from src.prompting.abstracts.factory_products import SystemContentForPromptProduct


class ConcreteSystemContentForPromptProduct(SystemContentForPromptProduct):

    def __init__(self, content_for_prompt: str, is_valid: bool, error: Optional[str] = None):
        self._content_for_prompt = content_for_prompt
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._content_for_prompt

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
