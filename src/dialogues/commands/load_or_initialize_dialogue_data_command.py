from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.dialogues.transcription import Transcription


class LoadOrInitializeDialogueDataCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        transcription: Transcription,
        load_data_from_ongoing_dialogue_command_factory: LoadDataFromOngoingDialogueCommandFactory,
        choose_participants_strategy: ChooseParticipantsStrategy,
        dialogue_manager: Optional[DialogueManager] = None,
        ongoing_dialogue_repository: Optional[OngoingDialogueRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(player_identifier, "player_identifier")

        self._player_identifier = player_identifier
        self._participants = participants
        self._transcription = transcription
        self._load_data_from_ongoing_dialogue_command_factory = (
            load_data_from_ongoing_dialogue_command_factory
        )
        self._choose_participants_strategy = choose_participants_strategy

        self._dialogue_manager = dialogue_manager or DialogueManager(playthrough_name)
        self._ongoing_dialogue_repository = (
            ongoing_dialogue_repository or OngoingDialogueRepository(playthrough_name)
        )

    def execute(self) -> None:
        if self._ongoing_dialogue_repository.has_participants():
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
