from typing import List, Optional

from src.base.required_string import RequiredString


class PlotBlueprintsProduct:
    def __init__(
        self,
        plot_blueprints: Optional[List[RequiredString]],
        is_valid: bool,
        error: Optional[str] = None,
    ):
        self._plot_blueprints = plot_blueprints
        self._is_valid = is_valid
        self._error = error

    def get(self) -> List[RequiredString]:
        return self._plot_blueprints

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
