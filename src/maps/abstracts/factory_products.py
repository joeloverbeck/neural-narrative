from abc import ABC, abstractmethod
from typing import Protocol

from src.maps.enums import RandomPlaceTypeMapEntryCreationResultType


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


class RandomPlaceTypeMapEntryCreationResult(Protocol):

    def get_result_type(self) -> RandomPlaceTypeMapEntryCreationResultType:
        pass

    def get_error(self) -> str:
        pass


class CardinalConnectionCreationProduct(Protocol):

    def was_successful(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
