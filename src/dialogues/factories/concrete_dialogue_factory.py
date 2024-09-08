from typing import List, Optional, Any

from openai import OpenAI

from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy
from src.dialogues.commands.speech_turn_produce_messages_to_prompt_llm_command import \
    SpeechTurnProduceMessagesToPromptLlmCommand
from src.dialogues.dialogues import compose_speech_entry
from src.dialogues.factories.llm_speech_data_factory import LlmSpeechDataFactory
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.dialogues.strategies.concrete_determine_system_message_for_speech_turn_strategy import \
    ConcreteDetermineSystemMessageForSpeechTurnStrategy
from src.dialogues.strategies.concrete_determine_user_messages_for_speech_turn_strategy import \
    ConcreteDetermineUserMessagesForSpeechTurnStrategy


class ConcreteDialogueFactory(DialogueFactory, Subject):
    def __init__(self, client: OpenAI, model: str, playthrough_name: str, participants: List[int],
                 player_identifier: Optional[int],
                 involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy):
        assert client
        assert model
        assert playthrough_name
        assert len(participants) >= 2
        assert involve_player_in_dialogue_strategy

        self._client = client
        self._model = model
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._player_identifier = player_identifier
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy

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
            player_input_product = self._involve_player_in_dialogue_strategy.do_algorithm(previous_messages, dialogue)

            if player_input_product.is_goodbye():
                break

            SpeechTurnProduceMessagesToPromptLlmCommand(self._playthrough_name, self._client, self._model,
                                                        self._player_identifier, self._participants, dialogue,
                                                        ConcreteDetermineSystemMessageForSpeechTurnStrategy(
                                                            self._playthrough_name, self._participants,
                                                            previous_messages),
                                                        ConcreteDetermineUserMessagesForSpeechTurnStrategy(
                                                            self._playthrough_name,
                                                            self._player_identifier,
                                                            player_input_product,
                                                            previous_messages)).execute()

            speech_data_product = LlmSpeechDataFactory(self._client, self._model,
                                                       previous_messages).create_speech_data()

            if not speech_data_product.is_valid():
                print(f"Failed to produce speech data: {speech_data_product.get_error()}")
                break

            dialogue.append(
                compose_speech_entry(speech_data_product))

            self.notify(speech_data_product.get())

        return ConcreteDialogueProduct(dialogue)
