import logging.config
import random
from typing import Optional

from src.base.abstracts.command import Command
from src.base.builders.playthrough_metadata_builder import PlaythroughMetadataBuilder
from src.base.constants import (
    DEFAULT_PLAYER_IDENTIFIER,
    DEFAULT_CURRENT_PLACE,
    DEFAULT_IDENTIFIER,
)
from src.base.enums import TemplateType
from src.base.exceptions import (
    StoryUniverseTemplateNotFoundError,
    PlaythroughAlreadyExistsError,
)
from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    write_json_file,
    create_directories,
    create_empty_json_file_if_not_exists,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class CreatePlaythroughMetadataCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        story_universe_template: str,
        filesystem_manager: Optional[FilesystemManager] = None,
        templates_repository: Optional[TemplatesRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(story_universe_template, "story_universe_template")

        self._playthrough_name = playthrough_name
        self._story_universe_template = story_universe_template

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._templates_repository = templates_repository or TemplatesRepository()
        self._path_manager = path_manager or PathManager()

    def _validate_playthrough_does_not_exist(self) -> None:
        # First ensure that the playthroughs dir exists.
        create_directories(self._path_manager.get_playthroughs_path())

        playthrough_exists = self._filesystem_manager.playthrough_exists(
            self._playthrough_name
        )

        if playthrough_exists:
            raise PlaythroughAlreadyExistsError(
                f"A playthrough with the name '{self._playthrough_name}' already exists."
            )
        else:
            # if it doesn't exist, we must create it.
            create_directories(
                self._path_manager.get_playthrough_path(self._playthrough_name)
            )

    def _validate_story_universe_template_exists(self) -> None:
        story_universe_templates = self._templates_repository.load_templates(
            TemplateType.STORY_UNIVERSE
        )

        if self._story_universe_template not in story_universe_templates:
            raise StoryUniverseTemplateNotFoundError(
                f"There is no such story universe template '{self._story_universe_template}'."
            )

    def _build_and_save_playthrough_metadata(self) -> None:
        random_hour = random.randint(0, 23)
        playthrough_metadata = (
            PlaythroughMetadataBuilder()
            .set_story_universe_template(self._story_universe_template)
            .set_player_identifier(DEFAULT_PLAYER_IDENTIFIER)
            .set_followers([])
            .set_current_place(DEFAULT_CURRENT_PLACE)
            .set_time_hour(random_hour)
            .set_last_identifiers(DEFAULT_IDENTIFIER, DEFAULT_IDENTIFIER)
            .build()
        )

        metadata_path = self._path_manager.get_playthrough_metadata_path(
            self._playthrough_name
        )

        write_json_file(metadata_path, playthrough_metadata)

    def _save_empty_map_file(self) -> None:
        map_path = self._path_manager.get_map_path(self._playthrough_name)

        create_empty_json_file_if_not_exists(map_path)

    def _log_playthrough_creation_success(self) -> None:
        playthrough_path = self._path_manager.get_playthrough_path(
            self._playthrough_name
        )

        logger.info(
            f"Playthrough '{self._playthrough_name}' created successfully at {playthrough_path}."
        )

    def execute(self) -> None:
        self._validate_playthrough_does_not_exist()
        self._validate_story_universe_template_exists()

        create_directories(
            self._path_manager.get_playthrough_path(self._playthrough_name)
        )

        try:
            self._build_and_save_playthrough_metadata()
            self._save_empty_map_file()
        except IOError as e:
            logger.error(f"Failed to save playthrough files: {e}")
            raise

        self._log_playthrough_creation_success()
