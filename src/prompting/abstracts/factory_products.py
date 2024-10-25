from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, Union

from pydantic import BaseModel


class LlmToolResponseProduct(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """

    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class LlmContentProduct(ABC):

    @abstractmethod
    def get(self) -> Union[str, BaseModel]:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class UserContentForCharacterGenerationProduct(Protocol):

    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass


class FilteredPlaceDescriptionGenerationProduct(Protocol):

    def get(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def get_error(self) -> str:
        pass
