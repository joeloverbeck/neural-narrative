from typing import Optional
from src.maps.abstracts.factory_products import PlaceDataProduct


class ConcretePlaceDataProduct(PlaceDataProduct):

    def __init__(self, place_data: dict, is_valid: bool, error: Optional[
        str] = None):
        assert place_data
        assert is_valid
        self._place_data = place_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._place_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
