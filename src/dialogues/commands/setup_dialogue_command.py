from typing import Optional

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
    MessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.commands.launch_dialogue_command import LaunchDialogueCommand
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import (
    HandlePossibleExistenceOfOngoingConversationCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class SetupDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        purpose: Optional[str],
        dialogue_observer: Observer,
        player_input_factory: PlayerInputFactory,
        handle_possible_existence_of_ongoing_conversation_command_factory: HandlePossibleExistenceOfOngoingConversationCommandFactory,
        message_data_producer_for_introduce_player_input_into_dialogue_strategy: MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not player_identifier:
            raise ValueError("player_identifier must not be empty.")
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._purpose = purpose
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory
        (self._handle_possible_existence_of_ongoing_conversation_command_factory) = (
            handle_possible_existence_of_ongoing_conversation_command_factory
        )
        (
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy
        ) = message_data_producer_for_introduce_player_input_into_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )

    def execute(self) -> None:
        transcription = Transcription()
        self._handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command(
            transcription
        ).execute()
        LaunchDialogueCommand(
            self._playthrough_name,
            self._player_identifier,
            self._participants,
            self._purpose,
            transcription,
            self._dialogue_observer,
            self._player_input_factory,
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy,
            self._message_data_producer_for_speech_turn_strategy,
        ).execute()
