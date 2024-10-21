from src.base.required_string import RequiredString
from src.prompting.abstracts.factory_products import (
    FilteredPlaceDescriptionGenerationProduct,
)


class ConcreteFilteredPlaceDescriptionGenerationProduct(
    FilteredPlaceDescriptionGenerationProduct
):
    def __init__(
            self,
            filtered_place_description: RequiredString,
            is_valid: bool,
            error: str = None,
    ):
        self._filtered_place_description = filtered_place_description
        self._is_valid = is_valid
        self._error = error

    def get(self) -> RequiredString:
        return self._filtered_place_description

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
