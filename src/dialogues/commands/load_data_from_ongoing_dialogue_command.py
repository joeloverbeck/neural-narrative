from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager


class LoadDataFromOngoingDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        transcription: Transcription,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._transcription = transcription
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._path_manager = path_manager or PathManager()

    def execute(self) -> None:
        ongoing_dialogue_file = read_json_file(
            self._path_manager.get_ongoing_dialogue_path(self._playthrough_name)
        )

        for identifier, participant in ongoing_dialogue_file["participants"].items():
            self._participants.add_participant(
                identifier,
                participant["name"],
                participant["description"],
                participant["personality"],
                participant["equipment"],
                participant["health"],
                participant["voice_model"],
            )

        for speech_turn in ongoing_dialogue_file["transcription"]:
            self._transcription.add_line(speech_turn)
