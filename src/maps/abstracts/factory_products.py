from abc import ABC, abstractmethod


class PlaceDataProduct(ABC):
    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class CurrentPlaceProduct(ABC):
    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass
