from unittest.mock import MagicMock
from src.base.playthrough_manager import PlaythroughManager
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory


def test_generate_player_character_command_init():
    playthrough_name = "test_playthrough"
    user_content = "user content"
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
    )
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
    playthrough_name = "test_playthrough"
    user_content = "user content"
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
    )
    assert command._playthrough_manager == playthrough_manager
    assert command._characters_manager == characters_manager


def test_generate_player_character_command_execute():
    playthrough_name = "test_playthrough"
    user_content = "user content"
    generate_character_command_factory = MagicMock(spec=GenerateCharacterCommandFactory)
    hierarchy_manager_factory = MagicMock(spec=HierarchyManagerFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)
    playthrough_manager.get_current_place_identifier.return_value = "current_place_id"
    hierarchy_manager = MagicMock()
    hierarchy_manager_factory.create_hierarchy_manager.return_value = hierarchy_manager
    places_parameter = "places_parameter_value"
    hierarchy_manager.fill_places_templates_parameter.return_value = places_parameter
    generate_character_command = MagicMock()
    (
        generate_character_command_factory.create_generate_character_command.return_value
    ) = generate_character_command
    characters_manager.get_latest_character_identifier.return_value = (
        "latest_character_id"
    )
    command = GeneratePlayerCharacterCommand(
        playthrough_name,
        user_content,
        generate_character_command_factory,
        hierarchy_manager_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
    )
    command.execute()
    playthrough_manager.get_current_place_identifier.assert_called_once()
    hierarchy_manager_factory.create_hierarchy_manager.assert_called_once()
    hierarchy_manager.fill_places_templates_parameter.assert_called_once_with(
        "current_place_id"
    )
    generate_character_command_factory.create_generate_character_command.assert_called_once_with(
        places_parameter,
        place_character_at_current_place=False,
        user_content="user content",
    )
    generate_character_command.execute.assert_called_once()
    characters_manager.get_latest_character_identifier.assert_called_once()
    playthrough_manager.update_player_identifier.assert_called_once_with(
        "latest_character_id"
    )
