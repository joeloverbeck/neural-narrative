from __future__ import annotations

from abc import ABC, abstractmethod


class ToolResponseParsingProduct(ABC):
    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


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


class ExtractedDataProduct(ABC):

    @abstractmethod
    def get(self):
        pass


class LlmContentProduct(ABC):
    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class SystemContentForPromptProduct(ABC):
    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass
