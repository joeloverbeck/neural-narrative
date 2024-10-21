# test_generate_player_character_command.py

from unittest.mock import MagicMock

from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory


def test_generate_player_character_command_init():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    user_content = RequiredString("user content")
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)

    # Act
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
    )

    # Assert
    assert command._user_content == user_content
    assert (
        command._generate_character_command_factory
        == generate_character_command_factory
    )
    assert command._hierarchy_manager_factory == hierarchy_manager_factory
    assert isinstance(command._playthrough_manager, PlaythroughManager)
    assert isinstance(command._characters_manager, CharactersManager)
    assert command._playthrough_manager._playthrough_name == playthrough_name
    assert command._characters_manager._playthrough_name == playthrough_name


def test_generate_player_character_command_init_with_managers():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    user_content = RequiredString("user content")
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)

    # Act
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
    )

    # Assert
    assert command._playthrough_manager == playthrough_manager
    assert command._characters_manager == characters_manager


def test_generate_player_character_command_execute():
    # Arrange
    playthrough_name = RequiredString("test_playthrough")
    user_content = RequiredString("user content")

    # Create mocks for dependencies
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)

    # Set up mocks
    # Mock the playthrough_manager to return a place identifier
    playthrough_manager.get_current_place_identifier.return_value = "current_place_id"

    # Mock the hierarchy_manager to return places_parameter
    hierarchy_manager = MagicMock()
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager

    # Mock the fill_places_templates_parameter method
    places_parameter = "places_parameter_value"
    hierarchy_manager.fill_places_templates_parameter.return_value = places_parameter

    # Mock the generate_character_command_factory to return a command
    generate_character_command = MagicMock()
    generate_character_command_factory.create_generate_character_command.return_value = (
        generate_character_command
    )

    # Mock the characters_manager to return a character identifier
    characters_manager.get_latest_character_identifier.return_value = (
        "latest_character_id"
    )

    # Create the command
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
    )

    # Act
    command.execute()

    # Assert
    # Check that playthrough_manager.get_current_place_identifier was called
    playthrough_manager.get_current_place_identifier.assert_called_once()

    # Check that hierarchy_manager_factory.create_hierarchy_manager was called
    hierarchy_manager_factory.create_hierarchy_manager.assert_called_once()

    # Check that hierarchy_manager.fill_places_templates_parameter was called with RequiredString of the current place identifier
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        RequiredString("current_place_id")
    )

    # Check that generate_character_command_factory.create_generate_character_command was called with correct parameters
    generate_character_command_factory.create_generate_character_command.assert_called_once_with(
        places_parameter,
        place_character_at_current_place=False,
        user_content="user content",
    )

    # Check that the generated command's execute() method was called
    generate_character_command.execute.assert_called_once()

    # Check that characters_manager.get_latest_character_identifier was called
    characters_manager.get_latest_character_identifier.assert_called_once()

    # Check that playthrough_manager.update_player_identifier was called with the latest character identifier
    playthrough_manager.update_player_identifier.assert_called_once_with(
        "latest_character_id"
    )
