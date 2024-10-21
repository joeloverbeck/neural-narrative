from unittest.mock import Mock

import pytest

from src.base.commands.create_playthrough_command import CreatePlaythroughCommand


def test_create_playthrough_command_execute():
    # Create mock commands and factories
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
    map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        latest_identifier,
        None,
    )

    # Instantiate the command with mocks
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command
    create_playthrough_command.execute()

    # Check that create_playthrough_metadata_command.execute() was called once
    create_playthrough_metadata_command.execute.assert_called_once()

    # Check that create_initial_map_command.execute() was called once
    create_initial_map_command.execute.assert_called_once()

    # Check that map_manager_factory.create_map_manager() was called once
    map_manager_factory.create_map_manager.assert_called_once()

    # Check that map_manager.get_identifier_and_place_template_of_latest_map_entry() was called once
    map_manager.get_identifier_and_place_template_of_latest_map_entry.assert_called_once()

    # Check that visit_place_command_factory.create_visit_place_command was called with latest_identifier
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        latest_identifier
    )

    # Check that visit_place_command.execute() was called once
    visit_place_command.execute.assert_called_once()

    # Check that generate_player_character_command.execute() was called once
    generate_player_character_command.execute.assert_called_once()


def test_create_playthrough_command_exception_handling():
    # Test that an exception in create_playthrough_metadata_command is propagated
    create_playthrough_metadata_command = Mock()
    create_playthrough_metadata_command.execute.side_effect = Exception(
        "Metadata creation failed"
    )
    create_initial_map_command = Mock()
    generate_player_character_command = Mock()
    visit_place_command_factory = Mock()
    map_manager_factory = Mock()

    # Instantiate the command with mocks
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command and expect an exception
    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()

    assert str(exc_info.value) == "Metadata creation failed"

    # Ensure that subsequent commands were not called
    create_initial_map_command.execute.assert_not_called()
    generate_player_character_command.execute.assert_not_called()
    visit_place_command_factory.create_visit_place_command.assert_not_called()
    map_manager_factory.create_map_manager.assert_not_called()


def test_create_playthrough_command_call_order():
    # Create mock commands and factories with side effects to track order
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

    # Define side_effect to append and return the mock
    def create_visit_place_command_side_effect(_identifier):
        call_order.append("create_visit_place_command")
        return visit_place_command

    visit_place_command_factory.create_visit_place_command.side_effect = (
        create_visit_place_command_side_effect
    )

    map_manager_factory = Mock()
    map_manager = Mock()
    map_manager.get_identifier_and_place_template_of_latest_map_entry.side_effect = (
        lambda: (
            call_order.append("get_latest_map_entry") or ("latest_identifier", None)
        )
    )

    def create_map_manager_side_effect():
        call_order.append("create_map_manager")
        return map_manager

    map_manager_factory.create_map_manager.side_effect = create_map_manager_side_effect

    # Instantiate the command with mocks
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command=create_playthrough_metadata_command,
        create_initial_map_command=create_initial_map_command,
        generate_player_character_command=generate_player_character_command,
        visit_place_command_factory=visit_place_command_factory,
        map_manager_factory=map_manager_factory,
    )

    # Execute the command
    create_playthrough_command.execute()

    # Check the order of calls
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
    # Test behavior with a different latest_identifier
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
    map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        different_identifier,
        None,
    )

    # Instantiate the command with mocks
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )

    # Execute the command
    create_playthrough_command.execute()

    # Check that the visit_place_command_factory was called with the different identifier
    visit_place_command_factory.create_visit_place_command.assert_called_once_with(
        different_identifier
    )
    visit_place_command.execute.assert_called_once()


def test_create_playthrough_command_visit_place_exception():
    # Test that an exception in visit_place_command is propagated
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
    map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        latest_identifier,
        None,
    )

    # Instantiate the command with mocks
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )

    # Execute the command and expect an exception
    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()

    assert str(exc_info.value) == "Visit place failed"

    # Ensure that generate_player_character_command was not called
    generate_player_character_command.execute.assert_not_called()


def test_create_playthrough_command_generate_player_exception():
    # Test that an exception in generate_player_character_command is propagated
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
    map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        latest_identifier,
        None,
    )

    # Instantiate and execute
    create_playthrough_command = CreatePlaythroughCommand(
        create_playthrough_metadata_command,
        create_initial_map_command,
        generate_player_character_command,
        visit_place_command_factory,
        map_manager_factory,
    )

    with pytest.raises(Exception) as exc_info:
        create_playthrough_command.execute()

    assert str(exc_info.value) == "Generate player failed"
