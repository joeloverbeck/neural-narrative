from typing import Optional, List, Any

from src.abstracts.command import Command
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy, \
    DetermineSystemMessageForSpeechTurnStrategy
from src.prompting.factories.speech_turn_tool_response_factory import SpeechTurnToolResponseFactory


class ProduceMessagesToPromptLlmCommand(Command):
    def __init__(self, client, playthrough_name: str, player_identifier: Optional[int], participants: List[int],
                 dialogue: List[dict[Any, str]],
                 determine_system_message_for_speech_turn_strategy: DetermineSystemMessageForSpeechTurnStrategy,
                 determine_user_messages_for_speech_turn_strategy: DetermineUserMessagesForSpeechTurnStrategy):
        assert client
        assert playthrough_name
        assert len(participants) >= 2
        assert determine_system_message_for_speech_turn_strategy
        assert determine_user_messages_for_speech_turn_strategy

        self._client = client
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._dialogue = dialogue
        self._determine_system_message_for_speech_turn_strategy = determine_system_message_for_speech_turn_strategy
        self._determine_user_messages_for_speech_turn_strategy = determine_user_messages_for_speech_turn_strategy

    def execute(self) -> None:
        speech_turn_tool_response_product = SpeechTurnToolResponseFactory(self._client, self._playthrough_name,
                                                                          self._player_identifier,
                                                                          self._participants,
                                                                          self._dialogue).create_llm_response()

        if not speech_turn_tool_response_product.is_valid():
            raise ValueError(f"{speech_turn_tool_response_product.get_error()}")

        print(f"Speech turn: {speech_turn_tool_response_product.get()}")

        self._determine_system_message_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)

        self._determine_user_messages_for_speech_turn_strategy.do_algorithm(speech_turn_tool_response_product)
