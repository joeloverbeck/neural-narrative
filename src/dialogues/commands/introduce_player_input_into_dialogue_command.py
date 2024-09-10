from typing import List, Optional

from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.characters.characters import load_character_data
from src.dialogues.abstracts.factory_products import PlayerInputProduct


class IntroducePlayerInputIntoDialogueCommand(Command, Subject):

    def __init__(self, playthrough_name: str, player_identifier: Optional[int],
                 player_input_product: PlayerInputProduct, dialogue: List[str]):
        assert playthrough_name
        assert player_input_product

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._player_input_product = player_input_product
        self._dialogue = dialogue

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def execute(self) -> None:
        # There's a player, who is going to contribute to the conversation.
        player_character_data = load_character_data(self._playthrough_name,
                                                    self._player_identifier)

        # Append the user's line to the dialogue so that the speech turn tool takes it into consideration.
        self._dialogue.append(f"{player_character_data["name"]}: {self._player_input_product.get()}")

        speech_data = {"name": f"{player_character_data["name"]}",
                       "speech": f"{self._player_input_product.get()}",
                       "narration_text": ""}

        self.notify(speech_data)
