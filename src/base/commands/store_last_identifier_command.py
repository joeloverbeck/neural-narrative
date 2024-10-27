from typing import Optional

from src.base.abstracts.command import Command
from src.base.enums import IdentifierType
from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager


class StoreLastIdentifierCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        identifier_type: IdentifierType,
        new_id: int,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._identifier_type = identifier_type
        self._new_id = new_id

        self._path_manager = path_manager or PathManager()

    def execute(self) -> None:
        file_path = self._path_manager.get_playthrough_metadata_path(
            self._playthrough_name
        )

        json_data = read_json_file(file_path)

        if self._identifier_type == IdentifierType.CHARACTERS:
            json_data["last_identifiers"]["characters"] = str(self._new_id)
        elif self._identifier_type == IdentifierType.PLACES:
            json_data["last_identifiers"]["places"] = str(self._new_id)

        write_json_file(file_path, json_data)
