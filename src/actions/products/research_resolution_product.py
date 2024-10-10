from typing import Optional


class ResearchResolutionProduct:
    def __init__(
        self,
        narrative: str,
        outcome: str,
        consequences: str,
        is_valid: bool,
        error: Optional[str] = None,
    ):
        if not narrative:
            raise ValueError("narrative can't be empty.")
        if not outcome:
            raise ValueError("outcome can't be empty.")
        if not consequences:
            raise ValueError("consequences can't be empty.")

        self._narrative = narrative
        self._outcome = outcome
        self._consequences = consequences
        self._is_valid = is_valid
        self._error = error

    def get_narrative(self) -> str:
        return self._narrative

    def get_outcome(self) -> str:
        return self._outcome

    def get_consequences(self) -> str:
        return self._consequences

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
