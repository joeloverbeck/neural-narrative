from typing import Optional, List

from openai import OpenAI

from src.abstracts.command import Command
from src.constants import MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy, \
    DetermineSystemMessageForSpeechTurnStrategy
from src.prompting.factories.speech_turn_tool_response_factory import SpeechTurnChoiceToolResponseFactory


class SpeechTurnProduceMessagesToPromptLlmCommand(Command):
    def __init__(self, playthrough_name: str, client: OpenAI, model: str, player_identifier: Optional[int],
                 participants: List[int],
                 dialogue: List[str],
                 determine_system_message_for_speech_turn_strategy: DetermineSystemMessageForSpeechTurnStrategy,
                 determine_user_messages_for_speech_turn_strategy: DetermineUserMessagesForSpeechTurnStrategy):
        assert playthrough_name
        assert client
        assert model
        assert len(participants) >= 2
        assert determine_system_message_for_speech_turn_strategy
        assert determine_user_messages_for_speech_turn_strategy

        self._playthrough_name = playthrough_name
        self._client = client
        self._model = model
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue = dialogue
        self._determine_system_message_for_speech_turn_strategy = determine_system_message_for_speech_turn_strategy
        self._determine_user_messages_for_speech_turn_strategy = determine_user_messages_for_speech_turn_strategy

        self._max_retries = MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE

    def execute(self) -> None:

        while self._max_retries > 0:
            speech_turn_tool_response_product = SpeechTurnChoiceToolResponseFactory(self._playthrough_name,
                                                                                    self._client,
                                                                                    self._model,
                                                                                    self._player_identifier,
                                                                                    self._participants,
                                                                                    self._dialogue).create_llm_response()

            if self._max_retries <= 0:
                raise ValueError(
                    "Was unable to produce a valid character choice for the next speech turn of the dialogue.")
            elif not speech_turn_tool_response_product.is_valid():
                print(f"{speech_turn_tool_response_product.get_error()}")
                self._max_retries -= 1
            else:
                self._determine_system_message_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)
                self._determine_user_messages_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)
                break
