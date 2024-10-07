from typing import Optional


class GoalResolutionProduct:
    def __init__(
        self,
        narration: str,
        success_determination: str,
        resolution: str,
        is_valid: bool,
        error: Optional[str] = None,
    ):
        if not narration:
            raise ValueError("narration can't be empty.")
        if not success_determination:
            raise ValueError("success_determination can't be empty.")
        if not resolution:
            raise ValueError("resolution can't be empty.")

        self._data = {
            "narration": narration,
            "success_determination": success_determination,
            "resolution": resolution,
        }

        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
