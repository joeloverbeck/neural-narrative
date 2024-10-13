from unittest.mock import Mock

import pytest

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.exceptions import CharacterGenerationFailedError


def test_generate_character_command_success():
    # Setup
    playthrough_name = "test_playthrough"
    place_character_at_current_place = True

    # Mock the CharacterGenerationToolResponseProvider
    character_generation_tool_response_provider = Mock()
    llm_tool_response_product = Mock()
    llm_tool_response_product.is_valid.return_value = True
    llm_tool_response_product.get.return_value = {
        "name": "Test Character",
        "description": "A brave hero.",
        "personality": "Courageous and noble",
        # Include other necessary character data fields as needed
    }
    character_generation_tool_response_provider.create_llm_response.return_value = (
        llm_tool_response_product
    )

    # Mock the StoreGeneratedCharacterCommandFactory and its command
    store_generated_character_command = Mock()
    store_generated_character_command.execute = Mock()
    store_generate_character_command_factory = Mock()
    store_generate_character_command_factory.create_store_generated_character_command.return_value = (
        store_generated_character_command
    )

    # Mock the GenerateCharacterImageCommandFactory and its command
    generate_character_image_command = Mock()
    generate_character_image_command.execute = Mock()
    generate_character_image_command_factory = Mock()
    generate_character_image_command_factory.create_generate_character_image_command.return_value = (
        generate_character_image_command
    )

    # Mock the CharactersManager
    characters_manager = Mock()
    characters_manager.get_latest_character_identifier.return_value = "char_001"

    # Mock the MovementManager
    movement_manager = Mock()
    movement_manager.place_character_at_current_place = Mock()

    # Create the GenerateCharacterCommand instance
    command = GenerateCharacterCommand(
        playthrough_name=playthrough_name,
        character_generation_tool_response_provider=character_generation_tool_response_provider,
        store_generate_character_command_factory=store_generate_character_command_factory,
        generate_character_image_command_factory=generate_character_image_command_factory,
        place_character_at_current_place=place_character_at_current_place,
        characters_manager=characters_manager,
        movement_manager=movement_manager,
    )

    # Execute the command
    command.execute()

    # Assertions
    character_generation_tool_response_provider.create_llm_response.assert_called_once()
    llm_tool_response_product.is_valid.assert_called_once()
    llm_tool_response_product.get.assert_called_once()

    store_generate_character_command_factory.create_store_generated_character_command.assert_called_once_with(
        llm_tool_response_product.get.return_value
    )
    store_generated_character_command.execute.assert_called_once()

    generate_character_image_command_factory.create_generate_character_image_command.assert_called_once_with(
        "char_001"
    )
    generate_character_image_command.execute.assert_called_once()

    if place_character_at_current_place:
        movement_manager.place_character_at_current_place.assert_called_once_with(
            "char_001"
        )
    else:
        movement_manager.place_character_at_current_place.assert_not_called()


def test_generate_character_command_failure():
    # Setup
    playthrough_name = "test_playthrough"
    place_character_at_current_place = False

    # Mock the CharacterGenerationToolResponseProvider
    character_generation_tool_response_provider = Mock()
    llm_tool_response_product = Mock()
    llm_tool_response_product.is_valid.return_value = False
    llm_tool_response_product.get_error.return_value = (
        "LLM failed to generate character"
    )
    character_generation_tool_response_provider.create_llm_response.return_value = (
        llm_tool_response_product
    )

    # Mock the other dependencies
    store_generate_character_command_factory = Mock()
    generate_character_image_command_factory = Mock()
    characters_manager = Mock()
    movement_manager = Mock()

    # Create the GenerateCharacterCommand instance
    command = GenerateCharacterCommand(
        playthrough_name=playthrough_name,
        character_generation_tool_response_provider=character_generation_tool_response_provider,
        store_generate_character_command_factory=store_generate_character_command_factory,
        generate_character_image_command_factory=generate_character_image_command_factory,
        place_character_at_current_place=place_character_at_current_place,
        characters_manager=characters_manager,
        movement_manager=movement_manager,
    )

    # Execute the command and expect an exception
    with pytest.raises(CharacterGenerationFailedError):
        command.execute()

    # Assertions
    character_generation_tool_response_provider.create_llm_response.assert_called_once()
    llm_tool_response_product.is_valid.assert_called_once()

    # Ensure that other commands are not called due to failure
    store_generate_character_command_factory.create_store_generated_character_command.assert_not_called()
    generate_character_image_command_factory.create_generate_character_image_command.assert_not_called()
    movement_manager.place_character_at_current_place.assert_not_called()
