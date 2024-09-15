from abc import ABC, abstractmethod
from typing import Protocol

from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription


class DialogueProduct(Protocol):
    def get_messages_to_llm(self) -> MessagesToLlm:
        pass

    def get_transcription(self) -> Transcription:
        pass

    def has_ended(self) -> bool:
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
    def get(self) -> MessagesToLlm:
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
