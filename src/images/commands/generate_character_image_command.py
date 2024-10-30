import logging
from pathlib import Path
from typing import Optional

from src.base.abstracts.command import Command
from src.characters.models.character_description_for_portrait import (
    CharacterDescriptionForPortrait,
)
from src.filesystem.file_operations import (
    read_file,
    write_binary_file,
    copy_file,
    create_directories,
)
from src.filesystem.path_manager import PathManager
from src.images.configs.generate_character_image_command_config import (
    GenerateCharacterImageCommandConfig,
)
from src.images.configs.generate_character_image_command_factories_config import (
    GenerateCharacterImageCommandFactoriesConfig,
)

logger = logging.getLogger(__name__)


class GenerateCharacterImageCommand(Command):
    """
    Command to generate an image for a character.
    """

    def __init__(
        self,
        config: GenerateCharacterImageCommandConfig,
        factories_config: GenerateCharacterImageCommandFactoriesConfig,
        path_manager: Optional[PathManager] = None,
    ):
        self._config = config
        self._factories_config = factories_config

        self._path_manager = path_manager or PathManager()

    def _get_character(self):
        """
        Retrieves the character using the character factory.
        """
        return self._factories_config.character_factory.create_character(
            self._config.character_identifier
        )

    def _ensure_character_description(self, character) -> None:
        """
        Ensures that the character has a description for the portrait.
        If not, generates one and saves it.
        """
        if character.has_description_for_portrait():
            return
        description_provider = self._factories_config.character_description_provider_factory.create_provider(
            character
        )
        description_product = description_provider.generate_product(
            CharacterDescriptionForPortrait
        )
        character.update_data({"description_for_portrait": description_product.get()})
        character.save()

    def _generate_prompt(self, character) -> str:
        """
        Generates the image generation prompt using the character's description.
        """
        prompt_template = read_file(
            self._path_manager.get_image_generation_prompt_path()
        )
        return prompt_template.format(
            character_description=character.description_for_portrait
        )

    def _get_target_image_path(self) -> Path:
        """
        Determines the target path for the character image.
        """
        # Ensure the images directory exists.
        create_directories(
            self._path_manager.get_playthrough_images_path(
                self._config.playthrough_name
            )
        )

        return self._path_manager.get_character_image_path(
            self._config.playthrough_name, self._config.character_identifier
        )

    def _generate_image(self, prompt: str):
        """
        Generates the image using the provided prompt.
        """
        return self._factories_config.generated_image_factory.generate_image(prompt)

    def _handle_image_generation_failure(
        self, target_image_path: Path, image_product
    ) -> None:
        """
        Handles the scenario where image generation fails.
        Copies the default image to the target path.
        """
        error_message = image_product.get_error()
        logger.warning(
            f"Failed to generate image for character '{self._config.character_identifier}': {error_message}"
        )

        copy_file(self._path_manager.get_default_image_path(), target_image_path)

        logger.info(f"Default image applied at '{target_image_path}'.")

    def _download_and_save_image(self, image_product, target_image_path: Path) -> None:
        """
        Downloads the generated image and saves it to the target path.
        """
        image_url = image_product.get()
        content_product = self._factories_config.url_content_factory.get_url(image_url)
        if content_product.is_valid():
            write_binary_file(target_image_path, content_product.get())
            logger.info(f"Image saved at '{target_image_path}'.")
        else:
            error_message = content_product.get_error()
            logger.error(
                f"Failed to download image from '{image_url}': {error_message}"
            )
            raise Exception(
                f"Failed to download image from '{image_url}': {error_message}"
            )

    def execute(self) -> None:
        """
        Executes the command to generate a character image.
        """
        character = self._get_character()
        self._ensure_character_description(character)
        prompt = self._generate_prompt(character)
        target_image_path = self._get_target_image_path()
        image_product = self._generate_image(prompt)
        if not image_product.is_valid():
            self._handle_image_generation_failure(target_image_path, image_product)
            return
        self._download_and_save_image(image_product, target_image_path)
