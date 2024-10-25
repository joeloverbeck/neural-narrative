import logging
from typing import List

import instructor

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.base.abstracts.subject import Subject
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.factories.llm_speech_data_provider_factory import (
    LlmSpeechDataProviderFactory,
)
from src.dialogues.models.speech_turn import get_custom_speech_turn_class
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


class CreateSpeechTurnDataCommand(Command, Subject):

    def __init__(
        self,
        transcription: Transcription,
        speech_turn_choice_response: LlmToolResponseProduct,
        llm_speech_data_provider_factory: LlmSpeechDataProviderFactory,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        self._transcription = transcription
        self._speech_turn_choice_response = speech_turn_choice_response
        self._llm_speech_data_provider_factory = llm_speech_data_provider_factory
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )
        self._observers: List[Observer] = []

    def _fix_invalid_speech_data(self, speech_data_product):
        if not speech_data_product.is_valid():
            logger.error(
                "Failed to produce speech data: %s", speech_data_product.get_error()
            )

            # Could be that the internal dictionary is None.
            if not speech_data_product.get():
                speech_data_product.set({})

            # If it turns out that there isn't a name applied, we enter the name we have.
            if not "name" in speech_data_product.get():
                speech_data_product.get()[
                    "name"
                ] = self._speech_turn_choice_response.get()["name"]

            speech_data_product.get()[
                "narration_text"
            ] = f"{self._speech_turn_choice_response.get()["name"]} looks confused."
            speech_data_product.get()["speech"] = "I don't know what to say."

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
                self._speech_turn_choice_response.get()["identifier"],
                self._speech_turn_choice_response.get()["name"],
                self._transcription,
            ).generate_product(
                instructor.Maybe(
                    get_custom_speech_turn_class(
                        self._speech_turn_choice_response.get()["name"]
                    )
                )
            )
        )

        self._fix_invalid_speech_data(speech_data_product)

        if "name" in speech_data_product.get():
            name = speech_data_product.get()["name"]

            narration_text = speech_data_product.get()["narration_text"]

            # The narration is optional now, so only add it if it exists.
            if narration_text:
                # Add the speech turn to the transcription.
                self._transcription.add_speech_turn(
                    name,
                    f"*{narration_text}* {speech_data_product.get()['speech']}",
                )
            else:
                self._transcription.add_speech_turn(
                    name, f"{speech_data_product.get()['speech']}"
                )

            self.notify(
                self._message_data_producer_for_speech_turn_strategy.produce_message_data(
                    self._speech_turn_choice_response, speech_data_product
                )
            )
