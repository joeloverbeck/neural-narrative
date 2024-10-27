from typing import Optional

from src.base.abstracts.command import Command
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.characters.factories.character_factory import CharacterFactory
from src.filesystem.file_operations import copy_file, create_directories
from src.filesystem.path_manager import PathManager
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.images.commands.generate_character_image_command import (
    GenerateCharacterImageCommand,
)
from src.images.configs.generate_character_image_command_config import (
    GenerateCharacterImageCommandConfig,
)
from src.images.configs.generate_character_image_command_factories_config import (
    GenerateCharacterImageCommandFactoriesConfig,
)
from src.requests.abstracts.abstract_factories import UrlContentFactory


class GenerateCharacterImageCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_factory: CharacterFactory,
        character_description_provider_factory: CharacterDescriptionProviderFactory,
        generated_image_factory: GeneratedImageFactory,
        url_content_factory: UrlContentFactory,
        testing: bool = False,
    ):
        self._playthrough_name = playthrough_name
        self._character_factory = character_factory
        self._character_description_provider_factory = (
            character_description_provider_factory
        )
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory
        self._testing = testing

    def create_command(self, character_identifier: str) -> Command:
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")

        if not self._testing:
            return GenerateCharacterImageCommand(
                GenerateCharacterImageCommandConfig(
                    self._playthrough_name, character_identifier
                ),
                GenerateCharacterImageCommandFactoriesConfig(
                    self._character_factory,
                    self._character_description_provider_factory,
                    self._generated_image_factory,
                    self._url_content_factory,
                ),
            )

        class FakeCommand(Command):

            def __init__(
                self,
                playthrough_name: str,
                character_identifier_for_fake_command: str,
                path_manager: Optional[PathManager] = None,
            ):
                self._playthrough_name = playthrough_name
                self._character_identifier_for_fake_command = (
                    character_identifier_for_fake_command
                )

                self._path_manager = path_manager or PathManager()

            def execute(self) -> None:
                # Ensure the images directory exists.
                create_directories(
                    self._path_manager.get_playthrough_images_path(
                        self._playthrough_name
                    )
                )

                target_image_path = self._path_manager.get_character_image_path(
                    self._playthrough_name,
                    self._character_identifier_for_fake_command,
                )

                copy_file(
                    self._path_manager.get_default_image_path(), target_image_path
                )

        return FakeCommand(self._playthrough_name, character_identifier)
