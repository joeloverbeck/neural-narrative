import logging

from src.abstracts.command import Command
from src.constants import MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy, \
    DetermineSystemMessageForSpeechTurnStrategy
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


class SpeechTurnProduceMessagesToPromptLlmCommand(Command):
    def __init__(self, transcription: Transcription,
                 speech_turn_choice_tool_response_product: LlmToolResponseProduct,
                 determine_system_message_for_speech_turn_strategy: DetermineSystemMessageForSpeechTurnStrategy,
                 determine_user_messages_for_speech_turn_strategy: DetermineUserMessagesForSpeechTurnStrategy):
        self._transcription = transcription
        self._speech_turn_choice_tool_response_product = speech_turn_choice_tool_response_product
        self._determine_system_message_for_speech_turn_strategy = determine_system_message_for_speech_turn_strategy
        self._determine_user_messages_for_speech_turn_strategy = determine_user_messages_for_speech_turn_strategy

        self._max_retries = MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE

    def execute(self) -> None:
        self._determine_system_message_for_speech_turn_strategy.do_algorithm(
            self._speech_turn_choice_tool_response_product)
        self._determine_user_messages_for_speech_turn_strategy.do_algorithm(
            self._speech_turn_choice_tool_response_product)
