from typing import List, Any

from src.abstracts.command import Command
from src.characters.characters import load_character_data
from src.filesystem.filesystem_manager import FilesystemManager


class StoreDialoguesCommand(Command):
    def __init__(self, playthrough_name: str, participants: List[int], dialogue: List[dict[Any, str]]):
        assert playthrough_name
        assert participants
        assert len(participants) >= 2

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._dialogue = dialogue

    def execute(self) -> None:
        if not self._dialogue or len(self._dialogue) <= 4:
            print("Won't save an empty or insufficient dialogue.")
            return

        prettified_dialogue = ""

        for speech_turn in self._dialogue:
            for key, values in speech_turn.items():
                prettified_dialogue += f"{key}: {values}\n"

        prettified_dialogue += "\n"

        filesystem_manager = FilesystemManager()

        for participant in self._participants:
            character_dialogues_path = filesystem_manager.get_file_path_to_character_dialogues(self._playthrough_name,
                                                                                               character_identifier=participant,
                                                                                               character_data=load_character_data(
                                                                                                   self._playthrough_name,
                                                                                                   participant))

            filesystem_manager.write_file(character_dialogues_path, prettified_dialogue)
            print(f"Saved dialogue at '{character_dialogues_path}'.")
