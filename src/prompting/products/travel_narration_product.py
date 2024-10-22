class TravelNarrationProduct:

    def __init__(self, travel_narration: str, is_valid: bool, error: str = None):
        if not travel_narration:
            raise ValueError("travel_narration can't be empty.")
        self._travel_narration = travel_narration
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._travel_narration

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
