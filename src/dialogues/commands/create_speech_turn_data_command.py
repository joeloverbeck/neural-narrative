import logging
from typing import List

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.base.abstracts.subject import Subject
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.factories.llm_speech_data_provider_factory import (
    LlmSpeechDataProviderFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


class CreateSpeechTurnDataCommand(Command, Subject):

    def __init__(
        self,
        messages_to_llm: MessagesToLlm,
        transcription: Transcription,
        speech_turn_choice_response: LlmToolResponseProduct,
        llm_speech_data_provider_factory: LlmSpeechDataProviderFactory,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._speech_turn_choice_response = speech_turn_choice_response
        self._llm_speech_data_provider_factory = llm_speech_data_provider_factory
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )

        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: dict) -> None:
        for observer in self._observers:
            observer.update(message)

    def execute(self) -> None:
        speech_data_product = (
            self._llm_speech_data_provider_factory.create_llm_speech_data_provider(
                self._messages_to_llm
            ).create_speech_data()
        )

        if not speech_data_product.is_valid():
            logger.error(
                "Failed to produce speech data: %s", speech_data_product.get_error()
            )

            # There's no real recovery to speech data being invalid, so let's pretend that the character
            # doesn't know what to say at the moment.
            speech_data_product.get()["narration_text"] = f"Looks confused."
            speech_data_product.get()["speech"] = "I don't know what to say."

        narration_text = speech_data_product.get()["narration_text"]

        if not narration_text:
            logger.warning(
                f"Speech turn didn't produce narration text. Content: {speech_data_product.get()}"
            )

        name = speech_data_product.get()["name"]

        if not narration_text or narration_text.lower() == "none":
            speech_data_product.get()[
                "narration_text"
            ] = f"{name} takes a moment to speak."

        self._transcription.add_speech_turn(
            name,
            f"*{speech_data_product.get()['narration_text']}* {speech_data_product.get()['speech']}",
        )

        self.notify(
            self._message_data_producer_for_speech_turn_strategy.produce_message_data(
                self._speech_turn_choice_response, speech_data_product
            )
        )
