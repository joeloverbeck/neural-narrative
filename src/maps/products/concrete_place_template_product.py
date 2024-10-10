from typing import Optional

from src.maps.abstracts.factory_products import PlaceTemplateProduct


class ConcretePlaceTemplateProduct(PlaceTemplateProduct):
    def __init__(
        self, place_template: Optional[str], is_valid: bool, error: str = None
    ):
        self._place_template = place_template
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._place_template

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
