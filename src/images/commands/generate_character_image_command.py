import logging
import shutil

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.constants import DEFAULT_IMAGE_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.requests.abstracts.abstract_factories import UrlContentFactory

logger = logging.getLogger(__name__)


class GenerateCharacterImageCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        generated_image_factory: GeneratedImageFactory,
        url_content_factory: UrlContentFactory,
        characters_manager: CharactersManager = None,
        filesystem_manager: FilesystemManager = None,
    ):
        if not character_identifier:
            raise ValueError("character_identifier should not be empty.")
        if not generated_image_factory:
            raise ValueError("generated_image_factory should not be empty.")
        if not url_content_factory:
            raise ValueError("url_content_factory should not be empty.")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory
        self._character_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

        self._secret_key = self._filesystem_manager.load_openai_secret_key()

    def execute(self) -> None:
        character_data = self._character_manager.load_character_data(
            self._character_identifier
        )

        prompt = (
            "Create a close-up portrait, as it could appear in a painting or a photo ID, of the following character:\n"
            f"Name: {character_data['name']}\n"
            f"Description: {character_data['description']}\n"
            f"Personality: {character_data['personality']}\n"
            f"Equipment belonging to {character_data['name']}: {character_data['equipment']}\n"
            "Note: the equipment is only listed to influence the portrait of the character. "
            "Do not depict equipment separately to the character. Avoid generating text."
            "The resulting image should resemble a photo or portrait made of a candid moment."
        )

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
