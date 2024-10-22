from typing import Optional, List
from src.base.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.protocols import InvolvePlayerInDialogueStrategySubject
from src.dialogues.factories.introduce_player_input_into_dialogue_command_factory import \
    IntroducePlayerInputIntoDialogueCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription


class ConcreteInvolvePlayerInDialogueStrategy(
    InvolvePlayerInDialogueStrategySubject):

    def __init__(self, player_identifier: Optional[str],
                 player_input_factory: PlayerInputFactory,
                 introduce_player_input_into_dialogue_command_factory:
                 IntroducePlayerInputIntoDialogueCommandFactory):
        self._player_identifier = player_identifier
        self._player_input_factory = player_input_factory
        self._introduce_player_input_into_dialogue_command_factory = (
            introduce_player_input_into_dialogue_command_factory)
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def do_algorithm(self, messages_to_llm: MessagesToLlm, transcription:
    Transcription) -> PlayerInputProduct:
        player_input_product = self._player_input_factory.create_player_input()
        if player_input_product.is_goodbye():
            return player_input_product
        if self._player_identifier and not player_input_product.is_silent():
            introduce_player_input_into_dialogue_command = (self.
            _introduce_player_input_into_dialogue_command_factory.
            create_introduce_player_input_into_dialogue_command(
                player_input_product, transcription))
            for observer in self._observers:
                introduce_player_input_into_dialogue_command.attach(observer)
            introduce_player_input_into_dialogue_command.execute()
        return player_input_product
