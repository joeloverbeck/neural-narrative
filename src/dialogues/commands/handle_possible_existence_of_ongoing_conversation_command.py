import os
from pathlib import Path

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager


class HandlePossibleExistenceOfOngoingConversationCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        transcription: Transcription,
        load_data_from_ongoing_dialogue_command_factory: LoadDataFromOngoingDialogueCommandFactory,
        choose_participants_strategy: ChooseParticipantsStrategy,
        filesystem_manager: FilesystemManager = None,
        dialogue_manager: DialogueManager = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._transcription = transcription
        self._load_data_from_ongoing_dialogue_command_factory = (
            load_data_from_ongoing_dialogue_command_factory
        )
        self._choose_participants_strategy = choose_participants_strategy
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._dialogue_manager = dialogue_manager or DialogueManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        ongoing_dialogue_path = (
            self._filesystem_manager.get_file_path_to_ongoing_dialogue(
                self._playthrough_name
            )
        )
        if os.path.exists(ongoing_dialogue_path) and "participants" in read_json_file(
            Path(ongoing_dialogue_path)
        ):
            self._load_data_from_ongoing_dialogue_command_factory.create_load_data_from_ongoing_dialogue_command(
                self._transcription
            ).execute()
        else:
            chosen_participants = (
                self._choose_participants_strategy.choose_participants()
            )
            self._dialogue_manager.gather_participants_data(
                self._player_identifier, chosen_participants, self._participants
            )
