from abc import ABC, abstractmethod
from typing import List


class DialogueProduct(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """

    @abstractmethod
    def get(self) -> List[str]:
        pass


class PlayerInputProduct(ABC):
    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def is_goodbye(self) -> bool:
        pass

    @abstractmethod
    def is_quit(self) -> bool:
        pass

    @abstractmethod
    def is_silent(self) -> bool:
        pass


class InitialPromptingMessagesProduct(ABC):
    @abstractmethod
    def get(self) -> List[dict]:
        pass


class SpeechDataProduct(ABC):
    @abstractmethod
    def get(self) -> dict[str, str]:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class SummaryProduct(ABC):
    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass
