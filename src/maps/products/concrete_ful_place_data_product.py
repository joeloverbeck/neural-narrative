from src.maps.abstracts.factory_products import FullPlaceDataProduct


class ConcreteFullPlaceDataProduct(FullPlaceDataProduct):
    def __init__(self, full_place_data: dict, is_valid: bool, error: str = None):
        self._full_place_data = full_place_data
        self._is_valid = is_valid
        self._error = error

    def get(self) -> dict:
        return self._full_place_data

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
