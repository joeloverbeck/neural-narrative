import logging
import shutil

from src.abstracts.command import Command
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.constants import (
    DEFAULT_IMAGE_FILE,
    IMAGE_GENERATION_PROMPT_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.requests.abstracts.abstract_factories import UrlContentFactory

logger = logging.getLogger(__name__)


class GenerateCharacterImageCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_description_provider_factory: CharacterDescriptionProviderFactory,
        generated_image_factory: GeneratedImageFactory,
        url_content_factory: UrlContentFactory,
        characters_manager: CharactersManager = None,
        filesystem_manager: FilesystemManager = None,
    ):
        if not character_identifier:
            raise ValueError("character_identifier should not be empty.")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._character_description_provider_factory = (
            character_description_provider_factory
        )
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory
        self._character_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        self._secret_key = self._filesystem_manager.load_openai_secret_key()

    def execute(self) -> None:
        character = Character(self._playthrough_name, self._character_identifier)

        # The description for a portrait gets saved in character data,
        # in case image generation has failed.
        if not character.has_description_for_portrait():
            character_description_product = (
                self._character_description_provider_factory.create_provider(
                    character
                ).generate_product()
            )

            character.update_data(
                {"description_for_portrait": character_description_product.get()}
            )

            # Save the description for portrait to file.
            character.save()

        prompt = self._filesystem_manager.read_file(
            IMAGE_GENERATION_PROMPT_FILE
        ).format(character_description=character.description_for_portrait)

        target_image_path = self._filesystem_manager.get_file_path_to_character_image(
            self._playthrough_name, self._character_identifier
        )

        generated_image_product = self._generated_image_factory.generate_image(prompt)

        if not generated_image_product.is_valid():
            logger.warning(
                f"Wasn't able to generate a proper image for character {self._character_identifier}: {generated_image_product.get_error()}"
            )
            shutil.copy(DEFAULT_IMAGE_FILE, target_image_path)
            logger.info(f"Default image applied at '{target_image_path}'.")
            return

        url_content_product = self._url_content_factory.get_url(
            generated_image_product.get()
        )

        if url_content_product.is_valid():
            self._filesystem_manager.write_binary_file(
                target_image_path, url_content_product.get()
            )
            logger.info(f"Image saved at '{target_image_path}'.")
        else:
            raise Exception(
                f"Failed to download image from {generated_image_product.get()}: {url_content_product.get_error()}"
            )
