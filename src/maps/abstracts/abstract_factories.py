from abc import ABC, abstractmethod

from src.maps.abstracts.factory_products import CurrentLocationDataProduct, AreaDataProduct


class CurrentLocationDataFactory(ABC):
    @abstractmethod
    def create_current_location_data(self) -> CurrentLocationDataProduct:
        pass


class AreaDataFactory(ABC):
    @abstractmethod
    def create_area_data(self) -> AreaDataProduct:
        pass
