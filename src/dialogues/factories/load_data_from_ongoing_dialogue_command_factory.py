from src.base.required_string import RequiredString
from src.dialogues.commands.load_data_from_ongoing_dialogue_command import (
    LoadDataFromOngoingDialogueCommand,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class LoadDataFromOngoingDialogueCommandFactory:
    def __init__(self, playthrough_name: RequiredString, participants: Participants):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants

    def create_load_data_from_ongoing_dialogue_command(
            self, messages_to_llm: MessagesToLlm, transcription: Transcription
    ) -> LoadDataFromOngoingDialogueCommand:
        return LoadDataFromOngoingDialogueCommand(
            self._playthrough_name, self._participants, messages_to_llm, transcription
        )
