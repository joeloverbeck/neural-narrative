from typing import Optional
from src.dialogues.abstracts.factory_products import SummaryProduct


class ConcreteSummaryProduct(SummaryProduct):

    def __init__(self, summary: str, is_valid: bool, error: Optional[str] = None
                 ):
        assert summary
        assert is_valid
        self._summary = summary
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._summary

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
