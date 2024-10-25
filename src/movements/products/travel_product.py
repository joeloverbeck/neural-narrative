from src.base.validators import validate_non_empty_string


class TravelProduct:

    def __init__(self, narrative: str, outcome: str, is_valid: bool, error: str = None):
        validate_non_empty_string(narrative, "narrative")
        validate_non_empty_string(outcome, "outcome")

        self._narrative = narrative
        self._outcome = outcome

        self._is_valid = is_valid
        self._error = error

    def get_narrative(self) -> str:
        return self._narrative

    def get_outcome(self) -> str:
        return self._outcome

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
