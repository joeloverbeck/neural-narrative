from typing import cast
from unittest.mock import Mock

import pytest

from src.base.constants import IMAGE_GENERATION_PROMPT_FILE, DEFAULT_IMAGE_FILE
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


def test_execute_success():
    character = Mock()
    character.has_description_for_portrait.return_value = True
    character.description_for_portrait = "A brave knight in shining armor."
    character_factory = Mock()
    character_factory.create_character.return_value = character
    filesystem_manager = Mock()
    prompt_template_content = Mock()
    prompt_template_content = (
        "Create an image of the following character: {character_description}"
    )
    filesystem_manager.read_file.return_value = prompt_template_content
    target_image_path = Mock()
    target_image_path = "/path/to/character/image.png"
    filesystem_manager.get_file_path_to_character_image.return_value = target_image_path
    generated_image_factory = Mock()
    image_product = Mock()
    image_product.is_valid.return_value = True
    image_product.get.return_value = "http://example.com/generated_image.png"
    generated_image_factory.generate_image.return_value = image_product
    url_content_factory = Mock()
    content_product = Mock()
    content_product.is_valid.return_value = True
    content_product.get.return_value = b"image data"
    url_content_factory.get_url.return_value = content_product
    config = GenerateCharacterImageCommandConfig(
        playthrough_name="playthrough1", character_identifier="character1"
    )
    factories_config = GenerateCharacterImageCommandFactoriesConfig(
        character_factory=character_factory,
        character_description_provider_factory=Mock(),
        generated_image_factory=cast(GeneratedImageFactory, generated_image_factory),
        url_content_factory=cast(UrlContentFactory, url_content_factory),
    )
    command = GenerateCharacterImageCommand(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )
    command.execute()
    character_factory.create_character.assert_called_once_with("character1")
    filesystem_manager.read_file.assert_called_once_with(IMAGE_GENERATION_PROMPT_FILE)
    expected_prompt = prompt_template_content.format(
        character_description=character.description_for_portrait
    )
    generated_image_factory.generate_image.assert_called_once_with(expected_prompt)
    url_content_factory.get_url.assert_called_once_with(
        "http://example.com/generated_image.png"
    )
    filesystem_manager.write_binary_file.assert_called_once_with(
        target_image_path, content_product.get.return_value
    )


def test_execute_character_without_description():
    character = Mock()
    character.has_description_for_portrait.return_value = False
    character_factory = Mock()
    character_factory.create_character.return_value = character
    description_provider = Mock()
    description_product = Mock()
    description_product.get.return_value = "A wise old wizard with a long beard."
    description_provider.generate_product.return_value = description_product
    character_description_provider_factory = Mock()
    character_description_provider_factory.create_provider.return_value = (
        description_provider
    )
    filesystem_manager = Mock()
    prompt_template_content = Mock()
    prompt_template_content = (
        "Create an image of the following character: {character_description}"
    )
    filesystem_manager.read_file.return_value = prompt_template_content
    target_image_path = Mock()
    target_image_path = "/path/to/character/image.png"
    filesystem_manager.get_file_path_to_character_image.return_value = target_image_path
    generated_image_factory = Mock()
    image_product = Mock()
    image_product.is_valid.return_value = True
    image_product.get.return_value = "http://example.com/generated_image.png"
    generated_image_factory.generate_image.return_value = image_product
    url_content_factory = Mock()
    content_product = Mock()
    content_product.is_valid.return_value = True
    content_product.get.return_value = b"image data"
    url_content_factory.get_url.return_value = content_product
    config = GenerateCharacterImageCommandConfig(
        playthrough_name="playthrough1", character_identifier="character1"
    )
    factories_config = GenerateCharacterImageCommandFactoriesConfig(
        character_factory=character_factory,
        character_description_provider_factory=character_description_provider_factory,
        generated_image_factory=cast(GeneratedImageFactory, generated_image_factory),
        url_content_factory=cast(UrlContentFactory, url_content_factory),
    )
    command = GenerateCharacterImageCommand(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )
    command.execute()
    character_description_provider_factory.create_provider.assert_called_once_with(
        character
    )
    description_provider.generate_product.assert_called_once()
    character.update_data.assert_called_once_with(
        {"description_for_portrait": description_product.get.return_value}
    )
    character.save.assert_called_once()
    filesystem_manager.write_binary_file.assert_called_once()


def test_execute_image_generation_failure():
    character = Mock()
    character.has_description_for_portrait.return_value = True
    character.description_for_portrait = "A brave knight in shining armor."
    character_factory = Mock()
    character_factory.create_character.return_value = character
    filesystem_manager = Mock()
    prompt_template_content = Mock()
    prompt_template_content = (
        "Create an image of the following character: {character_description}"
    )
    filesystem_manager.read_file.return_value = prompt_template_content
    target_image_path = Mock()
    target_image_path = "/path/to/character/image.png"
    filesystem_manager.get_file_path_to_character_image.return_value = target_image_path
    generated_image_factory = Mock()
    image_product = Mock()
    image_product.is_valid.return_value = False
    image_product.get_error.return_value = "Image generation error"
    generated_image_factory.generate_image.return_value = image_product
    config = GenerateCharacterImageCommandConfig(
        playthrough_name="playthrough1", character_identifier="character1"
    )
    factories_config = GenerateCharacterImageCommandFactoriesConfig(
        character_factory=character_factory,
        character_description_provider_factory=Mock(),
        generated_image_factory=cast(GeneratedImageFactory, generated_image_factory),
        url_content_factory=cast(UrlContentFactory, Mock()),
    )
    command = GenerateCharacterImageCommand(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )
    command.execute()
    filesystem_manager.copy_file.assert_called_once_with(
        DEFAULT_IMAGE_FILE, target_image_path
    )
    filesystem_manager.write_binary_file.assert_not_called()


def test_execute_image_download_failure():
    character = Mock()
    character.has_description_for_portrait.return_value = True
    character.description_for_portrait = "A brave knight in shining armor."
    character_factory = Mock()
    character_factory.create_character.return_value = character
    filesystem_manager = Mock()
    prompt_template_content = (
        "Create an image of the following character: {character_description}"
    )
    filesystem_manager.read_file.return_value = prompt_template_content
    target_image_path = "/path/to/character/image.png"
    filesystem_manager.get_file_path_to_character_image.return_value = target_image_path
    generated_image_factory = Mock()
    image_product = Mock()
    image_product.is_valid.return_value = True
    image_product.get.return_value = "http://example.com/generated_image.png"
    generated_image_factory.generate_image.return_value = image_product
    url_content_factory = Mock()
    content_product = Mock()
    content_product.is_valid.return_value = False
    content_product.get_error.return_value = "Download failed"
    url_content_factory.get_url.return_value = content_product
    config = GenerateCharacterImageCommandConfig(
        playthrough_name="playthrough1", character_identifier="character1"
    )
    factories_config = GenerateCharacterImageCommandFactoriesConfig(
        character_factory=character_factory,
        character_description_provider_factory=Mock(),
        generated_image_factory=cast(GeneratedImageFactory, generated_image_factory),
        url_content_factory=cast(UrlContentFactory, url_content_factory),
    )
    command = GenerateCharacterImageCommand(
        config=config,
        factories_config=factories_config,
        filesystem_manager=filesystem_manager,
    )
    with pytest.raises(Exception) as exc_info:
        command.execute()
    assert (
        f"Failed to download image from 'http://example.com/generated_image.png': Download failed"
        in str(exc_info)
    )
    filesystem_manager.write_binary_file.assert_not_called()


def test_execute_character_factory_failure():
    character_factory = Mock()
    character_factory.create_character.side_effect = Exception("Character not found")
    config = GenerateCharacterImageCommandConfig(
        playthrough_name="playthrough1", character_identifier="character1"
    )
    factories_config = GenerateCharacterImageCommandFactoriesConfig(
        character_factory=character_factory,
        character_description_provider_factory=Mock(),
        generated_image_factory=cast(GeneratedImageFactory, Mock()),
        url_content_factory=cast(UrlContentFactory, Mock()),
    )
    command = GenerateCharacterImageCommand(
        config=config, factories_config=factories_config, filesystem_manager=Mock()
    )
    with pytest.raises(Exception) as exc_info:
        command.execute()
    assert "Character not found" in str(exc_info)
