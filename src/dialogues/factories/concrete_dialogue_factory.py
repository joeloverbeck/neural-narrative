from typing import List, Optional, Any

from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.commands.create_player_speech_data_command import CreatePlayerSpeechDataCommand
from src.dialogues.factories.concrete_player_input_factory import ConcretePlayerInputFactory
from src.dialogues.factories.llm_speech_data_factory import LlmSpeechDataFactory
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.prompting.factories.speech_turn_tool_response_factory import SpeechTurnToolResponseFactory


class ConcreteDialogueFactory(DialogueFactory, Subject):
    def __init__(self, client, playthrough_name: str, participants: List[int], player_identifier: Optional[int] = None):
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

    def create_dialogue(self) -> DialogueProduct:
        """Manage the conversation loop between user and character."""

        # Assuming that the player will have the first choice to talk,
        # once he does talk, the LLM should be prompted to decide who will speak next.
        previous_messages: List[dict] = []
        dialogue: List[dict[Any, str]] = []

        while True:
            player_input_product = ConcretePlayerInputFactory(
                "\nYour input [options: goodbye, silent]: ").create_player_input()

            if player_input_product.is_goodbye():
                break

            create_player_speech_data_command = CreatePlayerSpeechDataCommand(self._playthrough_name,
                                                                              self._player_identifier,
                                                                              player_input_product,
                                                                              previous_messages, dialogue)

            for observer in self._observers:
                create_player_speech_data_command.attach(observer)

            create_player_speech_data_command.execute()

            # We'll only do the prompting for the initial prompting messages for a dialogue when we know what character other than the player will be the next to speak.
            # Note: a couple of things could happen here: the player has spoken, or the player hasn't spoken.
            # Independently of those, we need to know what character other than the player will speak next.
            speech_turn_tool_response_product = SpeechTurnToolResponseFactory(self._client, self._playthrough_name,
                                                                              self._player_identifier,
                                                                              self._participants,
                                                                              dialogue).create_llm_response()

            if not speech_turn_tool_response_product.is_valid():
                print(speech_turn_tool_response_product.get_error())
                break

            print(f"Speech turn: {speech_turn_tool_response_product.get()}")

            llm_speech_data_factory = LlmSpeechDataFactory(self._client, self._playthrough_name,
                                                           self._player_identifier, self._participants,
                                                           player_input_product,
                                                           previous_messages,
                                                           speech_turn_tool_response_product.get(),
                                                           dialogue)

            for observer in self._observers:
                llm_speech_data_factory.attach(observer)

            speech_data_product = llm_speech_data_factory.create_speech_data()

            if not speech_data_product.is_valid():
                print(f"Failed to produce speech data: {speech_data_product.get_error()}")
                break

            dialogue.append(
                {speech_data_product.get()[
                     "name"]: f"*{speech_data_product.get()['narration_text']}* {speech_data_product.get()['speech']}"})

            self.notify(speech_data_product.get())

        return ConcreteDialogueProduct(dialogue)
