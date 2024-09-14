import logging
from typing import List

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class StoreDialoguesCommand(Command):
    def __init__(self, playthrough_name: str, participants: List[str], transcription: Transcription,
                 filesystem_manager: FilesystemManager = None, characters_manager: CharactersManager = None):
        assert playthrough_name
        assert participants
        assert len(participants) >= 2

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._transcription = transcription

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(self._playthrough_name)

    def execute(self) -> None:
        if not self._transcription.is_transcription_sufficient():
            logger.error("Won't save an empty or insufficient dialogue.")
            return

        prettified_dialogue = ""

        for speech_turn in self._transcription.get():
            prettified_dialogue += f"{speech_turn}\n"

        prettified_dialogue += "\n"

        for participant in self._participants:
            character_dialogues_path = self._filesystem_manager.get_file_path_to_character_dialogues(
                self._playthrough_name,
                character_identifier=participant,
                character_data=self._characters_manager.load_character_data(
                    self._playthrough_name,
                    participant))

            self._filesystem_manager.write_file(character_dialogues_path, prettified_dialogue)
            logger.info(f"Saved dialogue at '{character_dialogues_path}'.")
