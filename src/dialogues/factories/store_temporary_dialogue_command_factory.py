from typing import Optional

from src.base.validators import validate_non_empty_string
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class StoreTemporaryDialogueCommandFactory:
    def __init__(
        self, playthrough_name: str, participants: Participants, purpose: Optional[str]
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        if not participants.enough_participants():
            raise ValueError(
                f"There weren't enough participants for a dialogue: {participants.get()}"
            )

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose

    def create_command(
        self,
        transcription: Transcription,
    ):
        return StoreTemporaryDialogueCommand(
            self._playthrough_name,
            self._participants,
            self._purpose,
            transcription,
        )
