from typing import Optional
from src.maps.abstracts.factory_products import CurrentPlaceProduct


class ConcreteCurrentPlaceProduct(CurrentPlaceProduct):

    def __init__(self, current_place: dict, is_valid: bool, error: Optional
    [str] = None):
        assert current_place
        self._current_place = current_place
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._current_place

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
