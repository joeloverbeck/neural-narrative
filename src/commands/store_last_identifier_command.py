import os

from src.abstracts.command import Command
from src.constants import PLAYTHROUGHS_FOLDER, LAST_IDENTIFIERS_FILE
from src.enums import IdentifierType
from src.files import save_json_file, load_existing_or_new_json_file


class StoreLastIdentifierCommand(Command):
    def __init__(self, playthrough_name: str, identifier_type: IdentifierType, new_id: int):
        self._playthrough_name = playthrough_name
        self._identifier_type = identifier_type
        self._new_id = new_id

    def execute(self) -> None:
        # Define the file path
        file_path = os.path.join(PLAYTHROUGHS_FOLDER, self._playthrough_name, LAST_IDENTIFIERS_FILE)

        # Load the existing JSON data
        json_data = load_existing_or_new_json_file(file_path)

        # Update the identifier based on the identifier type
        if self._identifier_type == IdentifierType.CHARACTERS:
            json_data["characters"] = str(self._new_id)
        elif self._identifier_type == IdentifierType.PLACES:
            json_data["places"] = str(self._new_id)

        # Save the updated JSON data back to the file
        save_json_file(json_data, file_path)
