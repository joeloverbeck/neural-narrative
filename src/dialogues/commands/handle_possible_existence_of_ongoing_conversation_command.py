import os

from src.abstracts.command import Command
from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import \
    LoadDataFromOngoingDialogueCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager


class HandlePossibleExistenceOfOngoingConversationCommand(Command):
    def __init__(self, playthrough_name: str, player_identifier: str, participants: Participants,
                 messages_to_llm: MessagesToLlm, transcription: Transcription,
                 load_data_from_ongoing_dialogue_command_factory: LoadDataFromOngoingDialogueCommandFactory,
                 choose_participants_strategy: ChooseParticipantsStrategy,
                 filesystem_manager: FilesystemManager = None,
                 dialogue_manager: DialogueManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._load_data_from_ongoing_dialogue_command_factory = load_data_from_ongoing_dialogue_command_factory
        self._choose_participants_strategy = choose_participants_strategy

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._dialogue_manager = dialogue_manager or DialogueManager(self._playthrough_name)

    def execute(self) -> None:
        # It could be that there's an ongoing dialogue active.
        if os.path.exists(self._filesystem_manager.get_file_path_to_ongoing_dialogue(self._playthrough_name)):
            self._load_data_from_ongoing_dialogue_command_factory.create_load_data_from_ongoing_dialogue_command(
                self._messages_to_llm, self._transcription).execute()

        else:
            # Prompt for character(s) the user wishes to speak to
            chosen_participants = self._choose_participants_strategy.choose_participants()

            # gather participant data
            self._dialogue_manager.gather_participants_data(self._player_identifier, chosen_participants,
                                                            self._participants)
