from typing import List, Any

from src.abstracts.command import Command
from src.characters.characters import load_character_data
from src.files import get_file_path_to_character_dialogues, write_file


class StoreDialoguesCommand(Command):
    def __init__(self, playthrough_name: str, participants: List[int], dialogue: List[dict[Any, str]]):
        assert playthrough_name
        assert participants
        assert len(participants) >= 2
        assert dialogue
        assert len(dialogue) >= 4

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._dialogue = dialogue

    def execute(self) -> None:
        dialogue = ""

        for speech_turn in self._dialogue:
            for key, values in speech_turn.items():
                dialogue += f"{key}: {values}\n"

        for participant in self._participants:
            character_dialogues_path = get_file_path_to_character_dialogues(self._playthrough_name,
                                                                            character_identifier=participant,
                                                                            character_data=load_character_data(
                                                                                self._playthrough_name,
                                                                                participant))

            write_file(character_dialogues_path, dialogue)
            print(f"Saved dialogue at '{character_dialogues_path}'.")
