import logging.config

from src.base.commands.store_last_identifier_command import StoreLastIdentifierCommand
from src.base.enums import IdentifierType
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
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )
        try:
            current_value = int(
                playthrough_metadata["last_identifiers"][identifier_type]
            )
        except KeyError as error:
            logger.error(f"Key error: {error}")
            raise
        return current_value + 1

    def produce_and_update_next_identifier(
        self, identifier_type: IdentifierType
    ) -> int:
        next_identifier = self.determine_next_identifier(identifier_type)
        StoreLastIdentifierCommand(
            self._playthrough_name, identifier_type, next_identifier
        ).execute()
        return next_identifier