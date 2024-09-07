from src.abstracts.command import Command
from src.commands.store_last_identifier_command import StoreLastIdentifierCommand
from src.enums import IdentifierType
from src.files import load_existing_or_new_json_file, save_json_file, get_file_path_to_characters_file
from src.identifiers import determine_next_identifier


class StoreGeneratedCharacterCommand(Command):

    def __init__(self, playthrough_name: str, character_data: dict):
        assert playthrough_name
        assert character_data

        self._playthrough_name = playthrough_name
        self._character_data = character_data

    def execute(self) -> None:
        # Build the path to the characters.json file
        characters_file = get_file_path_to_characters_file(self._playthrough_name)

        characters = load_existing_or_new_json_file(characters_file)

        new_id = determine_next_identifier(self._playthrough_name, IdentifierType.CHARACTERS)

        # Given that a character is going to be added to file, the identifier on file for characters
        # should be changed.
        StoreLastIdentifierCommand(self._playthrough_name, IdentifierType.CHARACTERS, new_id).execute()

        # Add the new character entry
        characters[new_id] = self._character_data

        save_json_file(characters, characters_file)
