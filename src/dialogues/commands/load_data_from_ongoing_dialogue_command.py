from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.participants import Participants
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.dialogues.transcription import Transcription


class LoadDataFromOngoingDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        transcription: Transcription,
        ongoing_dialogue_repository: Optional[OngoingDialogueRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._participants = participants
        self._transcription = transcription

        self._ongoing_dialogue_repository = (
            ongoing_dialogue_repository or OngoingDialogueRepository(playthrough_name)
        )

    def execute(self) -> None:
        for (
            identifier,
            participant,
        ) in self._ongoing_dialogue_repository.get_participants().items():
            self._participants.add_participant(
                identifier,
                participant["name"],
                participant["description"],
                participant["personality"],
                participant["equipment"],
                participant["health"],
                participant["voice_model"],
            )

        for speech_turn in self._ongoing_dialogue_repository.get_transcription():
            self._transcription.add_line(speech_turn)
