from abc import ABC, abstractmethod
from typing import Protocol


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


class PlaceTemplateProduct(Protocol):
    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass


class FullPlaceDataProduct(Protocol):
    def get(self) -> dict:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
