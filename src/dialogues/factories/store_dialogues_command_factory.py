from typing import List

from src.dialogues.commands.store_dialogues_command import StoreDialoguesCommand
from src.dialogues.transcription import Transcription


class StoreDialoguesCommandFactory:
    def __init__(self, playthrough_name: str, participants: List[str]):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not len(participants) >= 2:
            raise ValueError("There weren't enough participants for the dialogue.")

        self._playthrough_name = playthrough_name
        self._participants = participants

    def create_store_dialogues_command(self, transcription: Transcription) -> StoreDialoguesCommand:
        return StoreDialoguesCommand(self._playthrough_name, self._participants, transcription)
