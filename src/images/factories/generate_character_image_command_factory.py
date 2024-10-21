import shutil
from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import DEFAULT_IMAGE_FILE
from src.base.required_string import RequiredString
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.abstracts.abstract_factories import (
    GeneratedImageFactory,
)
from src.images.commands.generate_character_image_command import (
    GenerateCharacterImageCommand,
)
from src.requests.abstracts.abstract_factories import UrlContentFactory


class GenerateCharacterImageCommandFactory:
    def __init__(
        self,
            playthrough_name: RequiredString,
        character_description_provider_factory: CharacterDescriptionProviderFactory,
        generated_image_factory: GeneratedImageFactory,
        url_content_factory: UrlContentFactory,
            testing: bool = False,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._character_description_provider_factory = (
            character_description_provider_factory
        )
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory

        self._testing = testing

    def create_command(self, character_identifier: RequiredString) -> Command:
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")
        if not self._testing:
            return GenerateCharacterImageCommand(
                self._playthrough_name,
                character_identifier,
                self._character_description_provider_factory,
                self._generated_image_factory,
                self._url_content_factory,
            )

        # If testing, we should return a fake GenerateCharacterImageCommand that doesn't
        # actually produce an image, which costs money.
        class FakeCommand(Command):
            def __init__(
                    self,
                    playthrough_name: RequiredString,
                    character_identifier_for_fake_command: RequiredString,
                    filesystem_manager: Optional[FilesystemManager] = None,
            ):
                self._playthrough_name = playthrough_name
                self._character_identifier_for_fake_command = (
                    character_identifier_for_fake_command
                )

                self._filesystem_manager = filesystem_manager or FilesystemManager()

            def execute(self) -> None:
                # Let's copy the default image.
                target_image_path = (
                    self._filesystem_manager.get_file_path_to_character_image(
                        self._playthrough_name.value,
                        self._character_identifier_for_fake_command.value,
                    )
                )
                shutil.copy(DEFAULT_IMAGE_FILE, target_image_path)

        return FakeCommand(self._playthrough_name, character_identifier)
