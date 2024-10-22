from src.dialogues.commands.store_dialogues_command import StoreDialoguesCommand
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class StoreDialoguesCommandFactory:

    def __init__(self, playthrough_name: str, participants: Participants):
        if not participants.enough_participants():
            raise ValueError('Not enough participants.')
        self._playthrough_name = playthrough_name
        self._participants = participants

    def create_store_dialogues_command(self, transcription: Transcription
                                       ) -> StoreDialoguesCommand:
        return StoreDialoguesCommand(self._playthrough_name, self.
                                     _participants, transcription)
