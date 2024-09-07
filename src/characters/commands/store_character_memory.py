from src.abstracts.command import Command
from src.characters.characters import load_character_data
from src.files import get_file_path_to_character_memories


class StoreCharacterMemory(Command):
    def __init__(self, playthrough_name: str, character_identifier: int, memory: str):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._memory = memory

    def execute(self) -> None:
        character_data = load_character_data(self._playthrough_name, self._character_identifier)

        # Open the file in append mode and write the memory
        with open(
                get_file_path_to_character_memories(self._playthrough_name, self._character_identifier, character_data),
                'a') as f:
            f.write(self._memory + '\n')
