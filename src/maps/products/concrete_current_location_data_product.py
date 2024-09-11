from typing import Optional

from src.maps.abstracts.factory_products import CurrentLocationDataProduct


class ConcreteCurrentLocationDataProduct(CurrentLocationDataProduct):
    def __init__(self, current_location_data: dict, is_valid: bool, error: Optional[str] = None):
        self._current_location_data = current_location_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._current_location_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
