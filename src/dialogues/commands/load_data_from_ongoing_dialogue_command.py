from typing import Optional
from src.base.abstracts.command import Command
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager


class LoadDataFromOngoingDialogueCommand(Command):

    def __init__(self, playthrough_name: str, participants: Participants,
                 messages_to_llm: MessagesToLlm, transcription: Transcription,
                 filesystem_manager: Optional[FilesystemManager] = None):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        ongoing_dialogue_file = (self._filesystem_manager.
                                 load_existing_or_new_json_file(self._filesystem_manager.
                                                                get_file_path_to_ongoing_dialogue(
            self._playthrough_name)))
        for identifier, participant in ongoing_dialogue_file['participants'
        ].items():
            self._participants.add_participant(identifier, participant[
                'name'], participant['description'], participant[
                                                   'personality'], participant['equipment'], participant[
                                                   'voice_model'])
        for message in ongoing_dialogue_file['messages_to_llm']:
            self._messages_to_llm.add_message(message['role'], message[
                'content'])
        for speech_turn in ongoing_dialogue_file['transcription']:
            self._transcription.add_line(speech_turn)
