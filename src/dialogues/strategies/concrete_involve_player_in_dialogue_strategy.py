from typing import Optional, List

from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy
from src.dialogues.commands.introduce_player_input_into_dialogue_command import IntroducePlayerInputIntoDialogueCommand
from src.dialogues.factories.concrete_player_input_factory import ConcretePlayerInputFactory


class ConcreteInvolvePlayerInDialogueStrategy(InvolvePlayerInDialogueStrategy, Subject):
    def __init__(self, client, playthrough_name: str, participants: List[int], player_identifier: Optional[int]):
        assert client
        assert playthrough_name
        assert len(participants) >= 2

        self._client = client
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._player_identifier = player_identifier

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def do_algorithm(self, previous_messages: List[dict], dialogue: List[str]) -> PlayerInputProduct:
        player_input_product = ConcretePlayerInputFactory(
            "\nYour input [options: goodbye, silent]: ").create_player_input()

        if player_input_product.is_goodbye():
            return player_input_product

        if self._player_identifier and not player_input_product.is_silent():
            introduce_player_input_into_dialogue_command = IntroducePlayerInputIntoDialogueCommand(
                self._playthrough_name, self._player_identifier, player_input_product, dialogue)

            for observer in self._observers:
                introduce_player_input_into_dialogue_command.attach(observer)

            introduce_player_input_into_dialogue_command.execute()

        return player_input_product
