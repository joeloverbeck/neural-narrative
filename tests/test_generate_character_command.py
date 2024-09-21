import logging
from unittest.mock import MagicMock, patch

import pytest

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.movement_manager import MovementManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.products.concrete_extracted_data_product import (
    ConcreteExtractedDataProduct,
)
from src.prompting.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)


def test_generate_character_command_invalid_llm_response(caplog):
    # Set up the mock character_generation_tool_response_provider
    mock_response_provider = MagicMock(spec=CharacterGenerationToolResponseProvider)
    mock_llm_tool_response_product = MagicMock(spec=LlmToolResponseProduct)
    mock_llm_tool_response_product.is_valid.return_value = False
    mock_llm_tool_response_product.get_error.return_value = "Some error occurred"
    mock_response_provider.create_llm_response.return_value = (
        mock_llm_tool_response_product
    )

    # Set up other dependencies as mocks
    mock_store_command_factory = MagicMock(spec=StoreGeneratedCharacterCommandFactory)
    mock_image_command_factory = MagicMock(spec=GenerateCharacterImageCommandFactory)
    mock_characters_manager = MagicMock(spec=CharactersManager)
    mock_movement_manager = MagicMock(spec=MovementManager)

    # Instantiate the command with mocks
    command = GenerateCharacterCommand(
        playthrough_name="test_playthrough",
        character_generation_tool_response_provider=mock_response_provider,
        store_generate_character_command_factory=mock_store_command_factory,
        generate_character_image_command_factory=mock_image_command_factory,
        characters_manager=mock_characters_manager,
        movement_manager=mock_movement_manager,
        place_character_at_current_place=True,
    )

    # Execute the command
    with caplog.at_level(logging.ERROR):
        command.execute()

    # Assertions
    assert (
        "The LLM was unable to generate a character: Some error occurred" in caplog.text
    )
    mock_store_command_factory.create_store_generated_character_command.assert_not_called()
    mock_image_command_factory.create_generate_character_image_command.assert_not_called()
    mock_movement_manager.place_character_at_current_place.assert_not_called()


def test_generate_character_command_valid_llm_response():
    # Set up the mock character_generation_tool_response_provider
    mock_response_provider = MagicMock(spec=CharacterGenerationToolResponseProvider)
    mock_llm_tool_response_product = MagicMock(spec=LlmToolResponseProduct)
    mock_llm_tool_response_product.is_valid.return_value = True
    mock_llm_tool_response_product.get.return_value = {
        "arguments": {"name": "Test Character"}
    }
    mock_response_provider.create_llm_response.return_value = (
        mock_llm_tool_response_product
    )

    # Mock the data extraction provider
    with patch(
        "src.prompting.providers.character_tool_response_data_extraction_provider.CharacterToolResponseDataExtractionProvider",
        autospec=True,
    ) as MockDataExtractionProvider:
        mock_data_extraction_instance = MockDataExtractionProvider.return_value
        mock_data_extraction_instance.extract_data.return_value = (
            ConcreteExtractedDataProduct({"name": "Test Character"})
        )

        # Set up other dependencies as mocks
        mock_store_command_factory = MagicMock(
            spec=StoreGeneratedCharacterCommandFactory
        )
        mock_store_command = MagicMock(spec=Command)
        mock_store_command_factory.create_store_generated_character_command.return_value = (
            mock_store_command
        )

        mock_image_command_factory = MagicMock(
            spec=GenerateCharacterImageCommandFactory
        )
        mock_image_command = MagicMock(spec=Command)
        mock_image_command_factory.create_generate_character_image_command.return_value = (
            mock_image_command
        )

        mock_characters_manager = MagicMock(spec=CharactersManager)
        mock_characters_manager.get_latest_character_identifier.return_value = 1

        mock_movement_manager = MagicMock(spec=MovementManager)

        # Instantiate the command with mocks
        command = GenerateCharacterCommand(
            playthrough_name="test_playthrough",
            character_generation_tool_response_provider=mock_response_provider,
            store_generate_character_command_factory=mock_store_command_factory,
            generate_character_image_command_factory=mock_image_command_factory,
            characters_manager=mock_characters_manager,
            movement_manager=mock_movement_manager,
            place_character_at_current_place=True,
        )

        # Execute the command
        command.execute()

        # Assertions
        mock_store_command_factory.create_store_generated_character_command.assert_called_once_with(
            {
                "name": "Test Character",
                "description": None,
                "personality": None,
                "profile": None,
                "likes": None,
                "dislikes": None,
                "first message": None,
                "speech patterns": None,
                "equipment": None,
            }
        )
        mock_store_command.execute.assert_called_once()

        mock_characters_manager.get_latest_character_identifier.assert_called()

        mock_image_command_factory.create_generate_character_image_command.assert_called_once_with(
            1
        )
        mock_image_command.execute.assert_called_once()

        mock_movement_manager.place_character_at_current_place.assert_called_once_with(
            1
        )


def test_generate_character_command_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        GenerateCharacterCommand(
            playthrough_name="",
            character_generation_tool_response_provider=MagicMock(
                spec=CharacterGenerationToolResponseProvider
            ),
            store_generate_character_command_factory=MagicMock(
                spec=StoreGeneratedCharacterCommandFactory
            ),
            generate_character_image_command_factory=MagicMock(
                spec=GenerateCharacterImageCommandFactory
            ),
            place_character_at_current_place=True,
        )
    assert "playthrough_name can't be empty." in str(exc_info.value)
