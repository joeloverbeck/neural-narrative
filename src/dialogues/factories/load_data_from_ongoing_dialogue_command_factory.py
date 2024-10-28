from src.base.validators import validate_non_empty_string
from src.dialogues.commands.load_data_from_ongoing_dialogue_command import (
    LoadDataFromOngoingDialogueCommand,
)
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class LoadDataFromOngoingDialogueCommandFactory:

    def __init__(self, playthrough_name: str, participants: Participants):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        if not isinstance(participants, Participants):
            raise TypeError(
                f"Expected 'participants' to be of type Participants, but was '{type(participants)}'."
            )

        self._playthrough_name = playthrough_name
        self._participants = participants

    def create_load_data_from_ongoing_dialogue_command(
        self, transcription: Transcription
    ) -> LoadDataFromOngoingDialogueCommand:
        return LoadDataFromOngoingDialogueCommand(
            self._playthrough_name, self._participants, transcription
        )
