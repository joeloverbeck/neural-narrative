import logging.config
from pathlib import Path

from src.base.enums import IdentifierType
from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class IdentifiersManager:

    def __init__(
        self, playthrough_name: str, filesystem_manager: FilesystemManager = None
    ):
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    @staticmethod
    def get_highest_identifier(data: dict) -> str:
        identifiers_int = [int(k) for k in data.keys()]
        max_id = max(identifiers_int)
        return str(max_id)

    def determine_next_identifier(self, identifier_type: IdentifierType) -> int:
        playthrough_metadata = read_json_file(
            Path(
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                )
            )
        )
        try:
            current_value = int(
                playthrough_metadata["last_identifiers"][identifier_type.value]
            )
        except KeyError as error:
            logger.error(f"Key error when determining next identifier: {error}")
            raise
        return current_value + 1
