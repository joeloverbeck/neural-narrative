from __future__ import annotations

from abc import ABC, abstractmethod

from src.dialogues.abstracts.factory_products import DialogueProduct, PlayerInputProduct, \
    InitialPromptingMessagesProduct, SpeechDataProduct


class DialogueFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract products. These products are called a family and are
    related by a high-level theme or concept. Products of one family are usually
    able to collaborate among themselves. A family of products may have several
    variants, but the products of one variant are incompatible with products of
    another.
    """

    @abstractmethod
    def create_dialogue(self) -> DialogueProduct:
        pass


class PlayerInputFactory(ABC):
    @abstractmethod
    def create_player_input(self) -> PlayerInputProduct:
        pass


class InitialPromptingMessagesFactory(ABC):
    @abstractmethod
    def create_initial_prompting_messages(self) -> InitialPromptingMessagesProduct:
        pass


class SpeechDataFactory(ABC):
    @abstractmethod
    def create_speech_data(self) -> SpeechDataProduct:
        pass
