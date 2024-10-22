from typing import Optional
from src.base.abstracts.command import Command
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager


class StoreTemporaryDialogueCommand(Command):

    def __init__(self, playthrough_name: str, participants: Participants,
                 purpose: Optional[str], messages_to_llm: MessagesToLlm,
                 transcription: Transcription, filesystem_manager: Optional[
                FilesystemManager] = None):
        if not participants.enough_participants():
            raise ValueError('Not enough participants.')
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        json_data = {'participants': self._participants.get(), 'purpose':
            self._purpose, 'messages_to_llm': self._messages_to_llm.get(),
                     'transcription': self._transcription.get()}
        self._filesystem_manager.save_json_file(json_data, self.
                                                _filesystem_manager.get_file_path_to_ongoing_dialogue_folder(
            self._playthrough_name))
