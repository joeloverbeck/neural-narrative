from typing import List, Optional

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.base.abstracts.subject import Subject
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy
from src.dialogues.transcription import Transcription


class IntroducePlayerInputIntoDialogueCommand(Command, Subject):

    def __init__(self, playthrough_name: str, player_identifier: Optional[
        str], player_input_product: PlayerInputProduct, transcription:
    Transcription,
                 message_data_producer_for_introduce_player_input_into_dialogue_strategy
                 : MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
                 characters_manager: CharactersManager = None):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._player_input_product = player_input_product
        self._transcription = transcription
        (self.
         _message_data_producer_for_introduce_player_input_into_dialogue_strategy
         ) = (
            message_data_producer_for_introduce_player_input_into_dialogue_strategy
        )
        self._observers: List[Observer] = []
        self._characters_manager = characters_manager or CharactersManager(self
                                                                           ._playthrough_name)

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def execute(self) -> None:
        player_character = Character(self._playthrough_name, self.
                                     _player_identifier)
        self._transcription.add_speech_turn(player_character.name, self.
                                            _player_input_product.get())
        self.notify(self.
                    _message_data_producer_for_introduce_player_input_into_dialogue_strategy
                    .produce_message_data(player_character, self._player_input_product)
                    )
