from unittest.mock import Mock, call

import pytest

from src.base.abstracts.command import Command
from src.maps.commands.process_search_for_place_command import (
    ProcessSearchForPlaceCommand,
)
from src.maps.commands.search_for_place_command import SearchForPlaceCommand
from src.maps.factories.attach_place_command_factory import AttachPlaceCommandFactory
from src.maps.factories.map_manager_factory import MapManagerFactory


@pytest.fixture
def search_for_place_command():
    return Mock(spec=SearchForPlaceCommand)


@pytest.fixture
def attach_place_command_factory():
    return Mock(spec=AttachPlaceCommandFactory)


@pytest.fixture
def map_manager():
    mock_map_manager = Mock()
    mock_map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        123,
        "template",
    )
    return mock_map_manager


@pytest.fixture
def map_manager_factory(map_manager):
    mock_factory = Mock(spec=MapManagerFactory)
    mock_factory.create_map_manager.return_value = map_manager
    return mock_factory


@pytest.fixture
def attach_place_command():
    mock_command = Mock(spec=Command)
    return mock_command


@pytest.fixture
def process_command(
    search_for_place_command,
    attach_place_command_factory,
    map_manager_factory,
    attach_place_command,
):
    # Configure the attach_place_command_factory to return attach_place_command
    attach_place_command_factory.create_command.return_value = attach_place_command

    return ProcessSearchForPlaceCommand(
        search_for_place_command=search_for_place_command,
        attach_place_command_factory=attach_place_command_factory,
        map_manager_factory=map_manager_factory,
    )


def test_execute_calls_search_for_place_command_execute(
    process_command, search_for_place_command
):
    process_command.execute()
    search_for_place_command.execute.assert_called_once()


def test_execute_calls_map_manager_factory_create_map_manager(
    process_command, map_manager_factory
):
    process_command.execute()
    map_manager_factory.create_map_manager.assert_called_once()


def test_execute_calls_get_identifier_and_place_template_of_latest_map_entry(
    process_command, map_manager
):
    process_command.execute()
    map_manager.get_identifier_and_place_template_of_latest_map_entry.assert_called_once()


def test_execute_creates_attach_place_command_with_new_id(
    process_command, attach_place_command_factory, map_manager
):
    process_command.execute()
    new_id, _ = (
        map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value
    )
    attach_place_command_factory.create_command.assert_called_once_with(new_id)


def test_execute_calls_attach_place_command_execute(
    process_command, attach_place_command
):
    process_command.execute()
    attach_place_command.execute.assert_called_once()


def test_execute_full_flow(
    process_command,
    search_for_place_command,
    map_manager_factory,
    map_manager,
    attach_place_command_factory,
    attach_place_command,
):
    process_command.execute()

    # Verify search_for_place_command.execute() was called
    search_for_place_command.execute.assert_called_once()

    # Verify map_manager_factory.create_map_manager() was called
    map_manager_factory.create_map_manager.assert_called_once()

    # Verify get_identifier_and_place_template_of_latest_map_entry() was called
    map_manager.get_identifier_and_place_template_of_latest_map_entry.assert_called_once()

    # Verify attach_place_command_factory.create_command() was called with correct new_id
    new_id, _ = (
        map_manager.get_identifier_and_place_template_of_latest_map_entry.return_value
    )
    attach_place_command_factory.create_command.assert_called_once_with(new_id)

    # Verify attach_place_command.execute() was called
    attach_place_command.execute.assert_called_once()


# Optional: Tests for edge cases (if applicable)


def test_execute_no_latest_map_entry(
    process_command, map_manager_factory, attach_place_command_factory
):
    # Configure map_manager to return None or raise an exception if no latest map entry
    map_manager_factory.create_map_manager.return_value.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        None,
        None,
    )

    # Depending on implementation, you might expect certain behavior.
    # Since the current implementation does not handle it, it might proceed to create_command with None.
    # You can test that create_command is called with None
    process_command.execute()
    attach_place_command_factory.create_command.assert_called_once_with(None)


def test_execute_attach_place_command_factory_called_after_search(
    process_command,
    search_for_place_command,
    map_manager_factory,
    attach_place_command_factory,
    attach_place_command,
):
    process_command.execute()

    # Ensure the order of calls: search_for_place_command.execute() before attach_place_command_factory.create_command()
    expected_calls = [
        call.execute(),
        call.create_map_manager(),
        call.get_identifier_and_place_template_of_latest_map_entry(),
        call.create_command(123),
        call.execute(),
    ]
    # Create a single mock to track all calls
    # Alternatively, assert the call order using separate mocks
    # Here, we check individual mocks as separate
    search_for_place_command.execute.assert_called_once()
    map_manager_factory.create_map_manager.assert_called_once()
    map_manager_factory.create_map_manager.return_value.get_identifier_and_place_template_of_latest_map_entry.assert_called_once()
    attach_place_command_factory.create_command.assert_called_once_with(123)
    attach_place_command.execute.assert_called_once()
