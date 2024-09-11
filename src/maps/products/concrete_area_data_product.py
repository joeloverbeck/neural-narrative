from typing import Optional

from src.maps.abstracts.factory_products import AreaDataProduct


class ConcreteAreaDataProduct(AreaDataProduct):
    def __init__(self, area_data: dict, is_valid: bool, error: Optional[str] = None):
        assert area_data
        assert is_valid

        self._area_data = area_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._area_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
