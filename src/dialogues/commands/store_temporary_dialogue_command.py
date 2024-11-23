import logging
from typing import Optional

from src.base.abstracts.command import Command
from src.dialogues.participants import Participants
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.dialogues.transcription import Transcription

logger = logging.getLogger(__name__)


class StoreTemporaryDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        purpose: Optional[str],
        transcription: Transcription,
        ongoing_dialogue_repository: Optional[OngoingDialogueRepository] = None,
    ):
        self._participants = participants
        self._purpose = purpose
        self._transcription = transcription
        self._ongoing_dialogue_repository = (
            ongoing_dialogue_repository or OngoingDialogueRepository(playthrough_name)
        )

    def execute(self) -> None:
        # if at this point we don't have enough participants, we have a problem.
        if not self._participants.enough_participants():
            raise ValueError(
                f"About to store the ongoing dialogue, there weren't enough participants. {self._participants.get()}"
            )

        self._ongoing_dialogue_repository.set_participants(self._participants.get())
        self._ongoing_dialogue_repository.set_purpose(self._purpose)
        self._ongoing_dialogue_repository.set_transcription(self._transcription.get())
