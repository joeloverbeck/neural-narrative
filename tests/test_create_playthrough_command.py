from unittest.mock import Mock

import pytest

from src.base.commands.create_playthrough_command import CreatePlaythroughCommand


def test_create_playthrough_command_execute():
    create_playthrough_metadata_command = Mock()
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    visit_place_command_factory = Mock()
    visit_place_command = Mock()
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )
    map_manager_factory = Mock()
    map_manager = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    latest_identifier = "latest_identifier"
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value) = (
        latest_identifier,
        None,
    )
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )
    create_playthrough_command.execute()
    create_playthrough_metadata_command.execute.assert_called_once()
    create_initial_map_command.execute.assert_called_once()
    map_manager_factory.create_map_manager.assert_called_once()
    map_manager.get_identifier_and_place_template_of_latest_map_entry.assert_called_once()
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        latest_identifier
    )
    visit_place_command.execute.assert_called_once()
    generate_player_character_command.execute.assert_called_once()


def test_create_playthrough_command_exception_handling():
    create_playthrough_metadata_command = Mock()
    create_playthrough_metadata_command.execute.side_effect = Exception(
        "Metadata creation failed"
    )
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    visit_place_command_factory = Mock()
    map_manager_factory = Mock()
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )
    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()
    assert "Metadata creation failed" in str(exc_info)
    create_initial_map_command.execute.assert_not_called()
    generate_player_character_command.execute.assert_not_called()
    visit_place_command_factory.create_visit_place_command.assert_not_called()
    map_manager_factory.create_map_manager.assert_not_called()


def test_create_playthrough_command_call_order():
    call_order = []
    create_playthrough_metadata_command = Mock()
    create_playthrough_metadata_command.execute.side_effect = lambda: call_order.append(
        "metadata"
    )
    create_initial_map_command = Mock()
    create_initial_map_command.execute.side_effect = lambda: call_order.append(
        "initial_map"
    )
    generate_player_character_command = Mock()
    generate_player_character_command.execute.side_effect = lambda: call_order.append(
        "generate_player"
    )
    visit_place_command_factory = Mock()
    visit_place_command = Mock()
    visit_place_command.execute.side_effect = lambda: call_order.append("visit_place")

    def create_visit_place_command_side_effect(_identifier):
        call_order.append("create_visit_place_command")
        return visit_place_command

    visit_place_command_factory.create_visit_place_command.side_effect = (
        create_visit_place_command_side_effect
    )
    map_manager_factory = Mock()
    map_manager = Mock()
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect) = (
        lambda: call_order.append("get_latest_map_entry") or ("latest_identifier", None)
    )

    def create_map_manager_side_effect():
        call_order.append("create_map_manager")
        return map_manager

    map_manager_factory.create_map_manager.side_effect = create_map_manager_side_effect
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )
    create_playthrough_command.execute()
    assert call_order == [
        "metadata",
        "initial_map",
        "create_map_manager",
        "get_latest_map_entry",
        "create_visit_place_command",
        "visit_place",
        "generate_player",
    ]


def test_create_playthrough_command_with_different_identifier():
    create_playthrough_metadata_command = Mock()
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    visit_place_command_factory = Mock()
    visit_place_command = Mock()
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )
    map_manager_factory = Mock()
    map_manager = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    different_identifier = "different_identifier"
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value) = (
        different_identifier,
        None,
    )
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )
    create_playthrough_command.execute()
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        different_identifier
    )
    visit_place_command.execute.assert_called_once()


def test_create_playthrough_command_visit_place_exception():
    create_playthrough_metadata_command = Mock()
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    visit_place_command_factory = Mock()
    visit_place_command = Mock()
    visit_place_command.execute.side_effect = Exception("Visit place failed")
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )
    map_manager_factory = Mock()
    map_manager = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    latest_identifier = "latest_identifier"
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value) = (
        latest_identifier,
        None,
    )
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )
    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()
    assert "Visit place failed" in str(exc_info)
    generate_player_character_command.execute.assert_not_called()


def test_create_playthrough_command_generate_player_exception():
    create_playthrough_metadata_command = Mock()
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    generate_player_character_command.execute.side_effect = Exception(
        "Generate player failed"
    )
    visit_place_command_factory = Mock()
    visit_place_command = Mock()
    visit_place_command_factory.create_visit_place_command.return_value = (
        visit_place_command
    )
    map_manager_factory = Mock()
    map_manager = Mock()
    map_manager_factory.create_map_manager.return_value = map_manager
    latest_identifier = "latest_identifier"
    (map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value) = (
        latest_identifier,
        None,
    )
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )
    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()
    assert "Generate player failed" in str(exc_info)
