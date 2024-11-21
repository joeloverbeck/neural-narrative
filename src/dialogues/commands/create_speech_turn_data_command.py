import logging
from typing import List, Dict

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.base.abstracts.subject import Subject
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.exceptions import InvalidSpeechDataError
from src.dialogues.factories.llm_speech_data_provider_factory import (
    LlmSpeechDataProviderFactory,
)
from src.dialogues.models.speech_turn import get_custom_speech_turn_class
from src.dialogues.transcription import Transcription
from src.dialogues.utils import format_speech
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


class CreateSpeechTurnDataCommand(Command, Subject):

    def __init__(
        self,
        transcription: Transcription,
        speech_turn_choice_response: LlmToolResponseProduct,
        summary_notes: Dict[str, Dict[str, str]],
        llm_speech_data_provider_factory: LlmSpeechDataProviderFactory,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        self._transcription = transcription
        self._speech_turn_choice_response = speech_turn_choice_response
        self._summary_notes = summary_notes
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
                self._speech_turn_choice_response.get()["identifier"],
                self._speech_turn_choice_response.get()["name"],
                self._transcription,
                self._summary_notes,
            ).generate_product(
                get_custom_speech_turn_class(
                    self._speech_turn_choice_response.get()["name"]
                )
            )
        )

        if not speech_data_product.is_valid():
            raise InvalidSpeechDataError(
                f"Failed to produce speech data: {speech_data_product.get_error()}",
            )

        if "name" in speech_data_product.get():
            name = speech_data_product.get()["name"]

            narration_text = speech_data_product.get()["narration_text"]

            speech_text = format_speech(
                narration_text, speech_data_product.get()["speech"]
            )

            self._transcription.add_speech_turn(name, speech_text)

            self.notify(
                self._message_data_producer_for_speech_turn_strategy.produce_message_data(
                    self._speech_turn_choice_response, speech_data_product
                )
            )
