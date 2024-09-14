import logging

from src.abstracts.command import Command
from src.constants import MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy, \
    DetermineSystemMessageForSpeechTurnStrategy
from src.dialogues.transcription import Transcription
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import \
    SpeechTurnChoiceToolResponseProviderFactory

logger = logging.getLogger(__name__)


class SpeechTurnProduceMessagesToPromptLlmCommand(Command):
    def __init__(self, transcription: Transcription,
                 speech_turn_choice_tool_response_factory: SpeechTurnChoiceToolResponseProviderFactory,
                 determine_system_message_for_speech_turn_strategy: DetermineSystemMessageForSpeechTurnStrategy,
                 determine_user_messages_for_speech_turn_strategy: DetermineUserMessagesForSpeechTurnStrategy):
        self._transcription = transcription
        self._speech_turn_choice_tool_response_factory = speech_turn_choice_tool_response_factory
        self._determine_system_message_for_speech_turn_strategy = determine_system_message_for_speech_turn_strategy
        self._determine_user_messages_for_speech_turn_strategy = determine_user_messages_for_speech_turn_strategy

        self._max_retries = MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE

    def execute(self) -> None:
        while self._max_retries > 0:
            speech_turn_tool_response_product = self._speech_turn_choice_tool_response_factory.create_speech_turn_choice_tool_response_provider(
                self._transcription).create_llm_response()

            if not speech_turn_tool_response_product.is_valid():
                logger.error(f"{speech_turn_tool_response_product.get_error()}")
                self._max_retries -= 1
                if self._max_retries == 0:
                    raise ValueError(
                        "Was unable to produce a valid character choice for the next speech turn of the dialogue."
                    )
            else:
                self._determine_system_message_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)
                self._determine_user_messages_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)
                break
