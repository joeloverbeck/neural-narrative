from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.base.abstracts.subject import Subject
from src.dialogues.abstracts.factory_products import (
    DialogueProduct,
    PlayerInputProduct,
    SummaryProduct,
)


class DialogueTurnFactory(Protocol):

    def process_turn_of_dialogue(self) -> DialogueProduct:
        pass


class PlayerInputFactory(ABC):

    @abstractmethod
    def create_player_input(self) -> PlayerInputProduct:
        pass


class DialogueSummaryProvider(Protocol):

    def create_summary(self) -> SummaryProduct:
        pass


class DialogueTurnFactorySubject(DialogueTurnFactory, Subject, Protocol):
    pass
