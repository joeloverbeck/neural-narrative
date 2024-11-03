from typing import Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import write_json_file, read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager


class StoreTemporaryDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        purpose: Optional[str],
        transcription: Transcription,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._transcription = transcription

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._path_manager = path_manager or PathManager()
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        # if at this point we don't have enough participants, we have a problem.
        if not self._participants.enough_participants():
            raise ValueError(
                f"About to store the ongoing dialogue, there weren't enough participants. {self._participants.get()}"
            )

        ongoing_dialogue_file_path = self._path_manager.get_ongoing_dialogue_path(
            self._playthrough_name
        )

        # Ensure not to overwrite the messages if there's an existing dialogue.
        if self._playthrough_manager.has_ongoing_dialogue():
            ongoing_dialogue_file = read_json_file(ongoing_dialogue_file_path)
        else:
            ongoing_dialogue_file = {}

        ongoing_dialogue_file.update(
            {
                "participants": self._participants.get(),
                "purpose": self._purpose,
                "transcription": self._transcription.get(),
            }
        )

        write_json_file(
            ongoing_dialogue_file_path,
            ongoing_dialogue_file,
        )
