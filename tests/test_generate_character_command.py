import logging
from unittest.mock import MagicMock

import pytest

from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.characters.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.movement_manager import MovementManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


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
