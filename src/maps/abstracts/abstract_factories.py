from abc import ABC, abstractmethod

from src.maps.abstracts.factory_products import PlaceDataProduct, CurrentPlaceProduct


class PlaceDataFactory(ABC):
    @abstractmethod
    def create_place_data(self) -> PlaceDataProduct:
        pass


class CurrentPlaceFactory(ABC):
    @abstractmethod
    def create_current_place(self) -> CurrentPlaceProduct:
        pass
