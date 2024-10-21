from typing import Optional, List

from src.base.required_string import RequiredString


class PlotTwistsProduct:

    def __init__(
        self,
        plot_twists: Optional[List[RequiredString]],
        is_valid: bool,
        error: Optional[str] = None,
    ):
        self._plot_twists = plot_twists
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[RequiredString]:
        return self._plot_twists

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
