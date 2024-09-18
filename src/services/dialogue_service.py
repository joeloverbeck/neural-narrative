from flask import url_for

from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import (
    HandlePossibleExistenceOfOngoingConversationCommandFactory,
)
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.factories.web_player_input_factory import WebPlayerInputFactory
from src.dialogues.observers.web_dialogue_observer import WebDialogueObserver
from src.dialogues.participants import Participants
from src.dialogues.strategies.web_choose_participants_strategy import (
    WebChooseParticipantsStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_introduce_player_input_into_dialogue_strategy import (
    WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_speech_turn_strategy import (
    WebMessageDataProducerForSpeechTurnStrategy,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.playthrough_manager import PlaythroughManager


class DialogueService:
    def __init__(self, playthrough_name, dialogue_participants):
        self._playthrough_name = playthrough_name
        self._dialogue_participants = dialogue_participants
        self._filesystem_manager = FilesystemManager()
        self._playthrough_manager = PlaythroughManager(playthrough_name)
        self._participants_instance = Participants()
        self._web_dialogue_observer = WebDialogueObserver()

    def process_user_input(self, user_input):
        # Create player input factory
        web_player_input_factory = WebPlayerInputFactory(user_input)
        player_input_product = web_player_input_factory.create_player_input()

        # Setup dialogue command
        setup_command = SetupDialogueCommand(
            self._playthrough_name,
            self._playthrough_manager.get_player_identifier(),
            self._participants_instance,
            self._web_dialogue_observer,
            web_player_input_factory,
            self.get_conversation_command_factory(),
            WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
            WebMessageDataProducerForSpeechTurnStrategy(
                self._playthrough_name,
                self._playthrough_manager.get_player_identifier(),
            ),
        )
        setup_command.execute()

        # Check if the input was "goodbye"
        is_goodbye = player_input_product.is_goodbye()

        # Prepare messages
        messages = self.prepare_messages()

        return messages, is_goodbye

    def get_conversation_command_factory(self):
        load_data_command_factory = LoadDataFromOngoingDialogueCommandFactory(
            self._playthrough_name, self._participants_instance
        )

        return HandlePossibleExistenceOfOngoingConversationCommandFactory(
            self._playthrough_name,
            self._playthrough_manager.get_player_identifier(),
            self._participants_instance,
            load_data_command_factory,
            WebChooseParticipantsStrategy(self._dialogue_participants),
        )

    def prepare_messages(self):
        messages = []
        for message in self._web_dialogue_observer.get_messages():
            message["sender_photo_url"] = url_for(
                "static", filename=message["sender_photo_url"]
            )
            messages.append(message)
        return messages
