import logging
import logging.config

from src.abstracts.command import Command
from src.enums import IdentifierType
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager

logger = logging.getLogger(__name__)


class StoreGeneratedCharacterCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_data: dict,
        filesystem_manager: FilesystemManager = None,
        identifiers_manager: IdentifiersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not character_data:
            raise ValueError("character_data can't be empty.")
        if not character_data["name"]:
            raise ValueError("malformed character_data.")

        self._playthrough_name = playthrough_name
        self._character_data = character_data
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )

        logging.config.dictConfig(self._filesystem_manager.get_logging_config_file())

    def execute(self) -> None:
        # Build the path to the characters.json file
        filesystem_manager = FilesystemManager()

        characters_file = filesystem_manager.get_file_path_to_characters_file(
            self._playthrough_name
        )

        characters = filesystem_manager.load_existing_or_new_json_file(characters_file)

        # Add the new character entry
        characters[
            self._identifiers_manager.produce_and_update_next_identifier(
                IdentifierType.CHARACTERS
            )
        ] = self._character_data

        filesystem_manager.save_json_file(characters, characters_file)

        logger.info(
            f"Saved character '{self._character_data["name"]}' at '{characters_file}'"
        )
