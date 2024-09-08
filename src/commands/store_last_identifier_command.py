from src.abstracts.command import Command
from src.enums import IdentifierType
from src.filesystem.filesystem_manager import FilesystemManager


class StoreLastIdentifierCommand(Command):
    def __init__(self, playthrough_name: str, identifier_type: IdentifierType, new_id: int):
        self._playthrough_name = playthrough_name
        self._identifier_type = identifier_type
        self._new_id = new_id

    def execute(self) -> None:
        # Define the file path
        filesystem_manager = FilesystemManager()

        file_path = filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name)

        # Load the existing JSON data
        json_data = filesystem_manager.load_existing_or_new_json_file(file_path)

        # Update the identifier based on the identifier type
        if self._identifier_type == IdentifierType.CHARACTERS:
            json_data["last_identifiers"]["characters"] = str(self._new_id)
        elif self._identifier_type == IdentifierType.PLACES:
            json_data["last_identifiers"]["places"] = str(self._new_id)

        # Save the updated JSON data back to the file
        filesystem_manager.save_json_file(json_data, file_path)
