from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.base.abstracts.subject import Subject
from src.dialogues.abstracts.factory_products import (
    DialogueProduct,
    PlayerInputProduct,
    InitialPromptingMessagesProduct,
    SpeechDataProduct,
    SummaryProduct,
)


class DialogueTurnFactory(Protocol):
    def process_turn_of_dialogue(self) -> DialogueProduct:
        pass


class PlayerInputFactory(ABC):
    @abstractmethod
    def create_player_input(self) -> PlayerInputProduct:
        pass


class InitialPromptingMessagesProvider(ABC):
    @abstractmethod
    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        pass


class SpeechDataFactory(ABC):
    @abstractmethod
    def create_speech_data(self) -> SpeechDataProduct:
        pass


class DialogueSummaryProvider(Protocol):
    def create_summary(self) -> SummaryProduct:
        pass


class DialogueTurnFactorySubject(DialogueTurnFactory, Subject, Protocol):
    pass
