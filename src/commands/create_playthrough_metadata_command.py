import logging
import logging.config
import os
import random

from src.abstracts.command import Command
from src.builders.playthrough_metadata_builder import PlaythroughMetadataBuilder
from src.constants import (
    DEFAULT_PLAYER_IDENTIFIER,
    DEFAULT_CURRENT_PLACE,
    DEFAULT_IDENTIFIER,
    WORLD_TEMPLATES_FILE,
)
from src.exceptions import (
    WorldTemplateNotFoundException,
    PlaythroughAlreadyExistsException,
)
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class CreatePlaythroughMetadataCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        world_template: str,
        filesystem_manager: FilesystemManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not world_template:
            raise ValueError("world_template must not be empty.")

        self._playthrough_name = playthrough_name
        self._world_template = world_template
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        logging.config.dictConfig(self._filesystem_manager.get_logging_config_file())

    def execute(self) -> None:
        # Check if the folder already exists
        if os.path.exists(
            self._filesystem_manager.get_file_path_to_playthrough_folder(
                self._playthrough_name
            )
        ):
            raise PlaythroughAlreadyExistsException(
                f"A playthrough with the name '{self._playthrough_name}' already exists."
            )

        # Checks here if there is such a world template:
        worlds_file = self._filesystem_manager.load_existing_or_new_json_file(
            WORLD_TEMPLATES_FILE
        )

        if self._world_template not in worlds_file:
            raise WorldTemplateNotFoundException(
                f"There is no such world template '{self._world_template}'"
            )

        # Create the playthrough folder
        os.makedirs(
            self._filesystem_manager.get_file_path_to_playthrough_folder(
                self._playthrough_name
            )
        )

        # Generate random hour and assign it as a string
        random_hour = random.randint(0, 23)

        metadata_builder = PlaythroughMetadataBuilder()
        playthrough_metadata = (
            metadata_builder.set_world_template(self._world_template)
            .set_player_identifier(DEFAULT_PLAYER_IDENTIFIER)
            .set_followers()
            .set_current_place(DEFAULT_CURRENT_PLACE)
            .set_time_hour(random_hour)
            .set_last_identifiers(DEFAULT_IDENTIFIER, DEFAULT_IDENTIFIER)
            .build()
        )

        # Save the metadata and map files
        try:
            # Write the initial values to the JSON file
            self._filesystem_manager.save_json_file(
                playthrough_metadata,
                self._filesystem_manager.get_file_path_to_playthrough_metadata(
                    self._playthrough_name
                ),
            )

            # Must also create the map JSON file
            self._filesystem_manager.save_json_file(
                {},
                self._filesystem_manager.get_file_path_to_map(self._playthrough_name),
            )
        except IOError as e:
            logger.error(f"Failed to save playthrough files: {e}")
            raise

        playthrough_path = self._filesystem_manager.get_file_path_to_playthrough_folder(
            self._playthrough_name
        )

        # Confirm that the playthrough has been successfully created
        logger.info(
            f"Playthrough '{self._playthrough_name}' created successfully at {playthrough_path}."
        )
