from typing import List, Optional

from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.characters.characters_manager import CharactersManager
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.transcription import Transcription


class IntroducePlayerInputIntoDialogueCommand(Command, Subject):

    def __init__(self, playthrough_name: str, player_identifier: Optional[str],
                 player_input_product: PlayerInputProduct, transcription: Transcription,
                 characters_manager: CharactersManager = None):

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._player_input_product = player_input_product
        self._transcription = transcription

        self._observers: List[Observer] = []

        self._characters_manager = characters_manager or CharactersManager(self._playthrough_name)

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def execute(self) -> None:
        # There's a player, who is going to contribute to the conversation.
        player_character_data = self._characters_manager.load_character_data(self._playthrough_name,
                                                                             self._player_identifier)

        # Append the user's line to the transcription so that the speech turn tool takes it into consideration.
        self._transcription.add_speech_turn(player_character_data["name"], self._player_input_product.get())

        speech_data = {"name": f"{player_character_data["name"]}",
                       "speech": f"{self._player_input_product.get()}",
                       "narration_text": ""}

        self.notify(speech_data)
