from typing import cast
from unittest.mock import Mock

import pytest

from src.abstracts.command import Command
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand
from src.dialogues.factories.store_dialogues_command_factory import StoreDialoguesCommandFactory
from src.dialogues.factories.summarize_dialogue_command_factory import SummarizeDialogueCommandFactory


@pytest.fixture
def mock_dialogue_factory():
    # Mock the DialogueFactory
    mock = Mock(DialogueFactory)
    dialogue_mock = Mock()
    dialogue_mock.get.return_value = "mocked_dialogue"
    mock.create_dialogue.return_value = dialogue_mock
    return mock


@pytest.fixture
def mock_summarize_dialogue_command_factory():
    # Mock the SummarizeDialogueCommandFactory
    mock = Mock(SummarizeDialogueCommandFactory)
    summarize_command_mock = Mock(Command)
    mock.create_summarize_dialogue_command.return_value = summarize_command_mock
    return mock


@pytest.fixture
def mock_store_dialogues_command_factory():
    # Mock the StoreDialoguesCommandFactory
    mock = Mock(StoreDialoguesCommandFactory)
    store_command_mock = Mock(Command)
    mock.create_store_dialogues_command.return_value = store_command_mock
    return mock


def test_produce_dialogue_command_execution(mock_dialogue_factory, mock_summarize_dialogue_command_factory,
                                            mock_store_dialogues_command_factory):
    # Cast the mocks to the expected types
    dialogue_factory = cast(DialogueFactory, mock_dialogue_factory)
    summarize_dialogue_command_factory = cast(SummarizeDialogueCommandFactory, mock_summarize_dialogue_command_factory)
    store_dialogues_command_factory = cast(StoreDialoguesCommandFactory, mock_store_dialogues_command_factory)

    # Create the ProduceDialogueCommand instance
    command = ProduceDialogueCommand(
        dialogue_factory=dialogue_factory,
        summarize_dialogue_command_factory=summarize_dialogue_command_factory,
        store_dialogues_command_factory=store_dialogues_command_factory
    )

    # Execute the command
    command.execute()

    # Check that dialogue_factory.create_dialogue() was called
    mock_dialogue_factory.create_dialogue.assert_called_once()

    # Check that summarize_dialogue_command_factory.create_summarize_dialogue_command() was called with the right argument
    mock_summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_called_once_with("mocked_dialogue")

    # Ensure the summarize command's execute was called
    mock_summarize_dialogue_command_factory.create_summarize_dialogue_command.return_value.execute.assert_called_once()

    # Check that store_dialogues_command_factory.create_store_dialogues_command() was called with the right argument
    mock_store_dialogues_command_factory.create_store_dialogues_command.assert_called_once_with("mocked_dialogue")

    # Ensure the store command's execute was called
    mock_store_dialogues_command_factory.create_store_dialogues_command.return_value.execute.assert_called_once()
