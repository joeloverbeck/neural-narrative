import logging
from typing import List

from src.abstracts.observer import Observer
from src.abstracts.subject import Subject
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy
from src.dialogues.factories.llm_speech_data_provider_factory import LlmSpeechDataProviderFactory
from src.dialogues.factories.speech_turn_produce_messages_to_prompt_llm_command_factory import \
    SpeechTurnProduceMessagesToPromptLlmCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.dialogues.transcription import Transcription

logger = logging.getLogger(__name__)


class ConcreteDialogueFactory(DialogueFactory, Subject):
    def __init__(self, involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategy,
                 speech_turn_produce_messages_to_prompt_llm_command_factory: SpeechTurnProduceMessagesToPromptLlmCommandFactory,
                 llm_speech_data_provider_factory: LlmSpeechDataProviderFactory):
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._speech_turn_produce_messages_to_prompt_llm_command_factory = speech_turn_produce_messages_to_prompt_llm_command_factory
        self._llm_speech_data_provider_factory = llm_speech_data_provider_factory

        self._observers: List[Observer] = []

        self._messages_to_llm = MessagesToLlm()
        self._transcription = Transcription()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def process_turn(self) -> bool:
        player_input_product = self._involve_player_in_dialogue_strategy.do_algorithm(self._messages_to_llm,
                                                                                      self._transcription)

        if player_input_product.is_goodbye():
            return False  # End dialogue

        # Proceed with the rest of the processing
        self._speech_turn_produce_messages_to_prompt_llm_command_factory.create_speech_turn_produce_messages_to_prompt_llm_command(
            self._messages_to_llm, self._transcription, player_input_product).execute()

        speech_data_product = self._llm_speech_data_provider_factory.create_llm_speech_data_provider(
            self._messages_to_llm).create_speech_data()

        if not speech_data_product.is_valid():
            logger.error(f"Failed to produce speech data: {speech_data_product.get_error()}")
            return False  # Or handle error appropriately

        self._transcription.add_speech_turn(speech_data_product.get()["name"],
                                            f"*{speech_data_product.get()['narration_text']}* {speech_data_product.get()['speech']}")

        self.notify(speech_data_product.get())

        return True  # Continue dialogue

    def create_dialogue(self) -> DialogueProduct:
        while True:
            continue_dialogue = self.process_turn()
            if not continue_dialogue:
                break

        return ConcreteDialogueProduct(self._transcription)
