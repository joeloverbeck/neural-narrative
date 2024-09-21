from src.prompting.abstracts.factory_products import (
    FilteredPlaceDescriptionGenerationProduct,
)


class ConcreteFilteredPlaceDescriptionGenerationProduct(
    FilteredPlaceDescriptionGenerationProduct
):
    def __init__(
        self, filtered_place_description: str, is_valid: bool, error: str = None
    ):
        if not filtered_place_description:
            raise ValueError("filtered_place_description can't be empty.")

        self._filtered_place_description = filtered_place_description
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._filtered_place_description

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error
