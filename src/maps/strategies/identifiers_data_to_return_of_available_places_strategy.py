from typing import Any

from src.maps.abstracts.strategies import DataToReturnOfAvailablePlacesStrategy


class IdentifiersDataToReturnOfAvailablePlacesStrategy(
    DataToReturnOfAvailablePlacesStrategy
):
    def data_to_return(self, available_places: dict[str, dict[str, Any]]) -> set[str]:
        return set(identifier for identifier, data in available_places.items())
