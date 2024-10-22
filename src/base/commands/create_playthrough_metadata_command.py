import logging.config
import random
from typing import Optional
from src.base.abstracts.command import Command
from src.base.builders.playthrough_metadata_builder import PlaythroughMetadataBuilder
from src.base.constants import DEFAULT_PLAYER_IDENTIFIER, DEFAULT_CURRENT_PLACE, DEFAULT_IDENTIFIER, \
    STORY_UNIVERSES_TEMPLATE_FILE
from src.base.exceptions import StoryUniverseTemplateNotFoundError, PlaythroughAlreadyExistsError
from src.filesystem.filesystem_manager import FilesystemManager
logger = logging.getLogger(__name__)


class CreatePlaythroughMetadataCommand(Command):

    def __init__(self, playthrough_name: str, story_universe_template: str,
                 filesystem_manager: Optional[FilesystemManager] = None):
        self._playthrough_name = playthrough_name
        self._story_universe_template = story_universe_template
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _validate_playthrough_does_not_exist(self) -> None:
        if self._filesystem_manager.playthrough_exists(self._playthrough_name):
            raise PlaythroughAlreadyExistsError(
                f"A playthrough with the name '{self._playthrough_name}' already exists."
            )

    def _validate_story_universe_template_exists(self) -> None:
        story_universe_templates = (self._filesystem_manager.
                                    load_existing_or_new_json_file(STORY_UNIVERSES_TEMPLATE_FILE))
        if self._story_universe_template not in story_universe_templates:
            raise StoryUniverseTemplateNotFoundError(
                f"There is no such story universe template '{self._story_universe_template}'."
            )

    def _build_and_save_playthrough_metadata(self) -> None:
        random_hour = random.randint(0, 23)
        playthrough_metadata = PlaythroughMetadataBuilder(
        ).set_story_universe_template(self._story_universe_template
                                      ).set_player_identifier(DEFAULT_PLAYER_IDENTIFIER).set_followers([]
                                                                                                       ).set_current_place(
            DEFAULT_CURRENT_PLACE).set_time_hour(
            random_hour).set_last_identifiers(DEFAULT_IDENTIFIER,
                                              DEFAULT_IDENTIFIER).build()
        metadata_path = (self._filesystem_manager.
                         get_file_path_to_playthrough_metadata(self._playthrough_name))
        self._filesystem_manager.save_json_file(playthrough_metadata,
                                                metadata_path)

    def _save_empty_map_file(self) -> None:
        map_path = self._filesystem_manager.get_file_path_to_map(self.
                                                                 _playthrough_name)
        self._filesystem_manager.save_json_file({}, map_path)

    def _log_playthrough_creation_success(self) -> None:
        playthrough_path = (self._filesystem_manager.
                            get_file_path_to_playthrough_folder(self._playthrough_name))
        logger.info(
            f"Playthrough '{self._playthrough_name}' created successfully at {playthrough_path}."
        )

    def execute(self) -> None:
        self._validate_playthrough_does_not_exist()
        self._validate_story_universe_template_exists()
        self._filesystem_manager.create_playthrough_folder(self.
                                                           _playthrough_name)
        try:
            self._build_and_save_playthrough_metadata()
            self._save_empty_map_file()
        except IOError as e:
            logger.error(f'Failed to save playthrough files: {e}')
            raise
        self._log_playthrough_creation_success()
