from typing import Protocol, Any


class DataToReturnOfAvailablePlacesStrategy(Protocol):
    def data_to_return(self, available_places: dict[str, dict[str, Any]]) -> set[str]:
        pass
