from typing import cast
from unittest.mock import patch, Mock

import pytest

from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.commands.end_dialogue_command import EndDialogueCommand


def test_execute_transcription_sufficient():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create a mock transcription that is sufficient
    mock_transcription = Mock()
    mock_transcription.is_transcription_sufficient.return_value = True

    # Create a mock DialogueProduct that returns the mock transcription
    mock_dialogue_product = Mock()
    mock_dialogue_product.get_transcription.return_value = mock_transcription

    # Create mock SummarizeDialogueCommand and its factory
    mock_summarize_dialogue_command = Mock()
    mock_summarize_dialogue_command_factory = Mock()
    mock_summarize_dialogue_command_factory.create_summarize_dialogue_command.return_value = (
        mock_summarize_dialogue_command
    )

    # Create mock StoreDialoguesCommand and its factory
    mock_store_dialogues_command = Mock()
    mock_store_dialogues_command_factory = Mock()
    mock_store_dialogues_command_factory.create_command.return_value = (
        mock_store_dialogues_command
    )

    # Create mock OngoingDialogueRepository
    mock_ongoing_dialogue_repository = Mock()

    # Create mock TimeManager
    mock_time_manager = Mock()

    # Create mock ConfigLoader that returns a specific time advancement
    mock_config_loader = Mock()
    time_advanced_due_to_dialogue = 2
    mock_config_loader.get_time_advanced_due_to_dialogue.return_value = (
        time_advanced_due_to_dialogue
    )

    # Create the EndDialogueCommand instance
    command = EndDialogueCommand(
        playthrough_name=playthrough_name,
        dialogue_product=cast(DialogueProduct, mock_dialogue_product),
        summarize_dialogue_command_factory=mock_summarize_dialogue_command_factory,
        store_dialogues_command_factory=mock_store_dialogues_command_factory,
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
        time_manager=mock_time_manager,
        config_loader=mock_config_loader,
    )

    # Act
    command.execute()

    # Assert
    # Ensure that is_transcription_sufficient was called
    mock_transcription.is_transcription_sufficient.assert_called_once()

    # Ensure that summarize_dialogue_command_factory was called with the correct transcription
    mock_summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_called_once_with(
        mock_transcription
    )
    # Ensure that summarize_dialogue_command's execute method was called
    mock_summarize_dialogue_command.execute.assert_called_once()

    # Ensure that store_dialogues_command_factory was called with the correct transcription
    mock_store_dialogues_command_factory.create_command.assert_called_once_with(
        mock_transcription
    )
    # Ensure that store_dialogues_command's execute method was called
    mock_store_dialogues_command.execute.assert_called_once()

    # Ensure that ongoing_dialogue_repository.remove_dialogue was called
    mock_ongoing_dialogue_repository.remove_dialogue.assert_called_once()

    # Ensure that time_manager.advance_time was called with the correct time
    mock_time_manager.advance_time.assert_called_once_with(
        time_advanced_due_to_dialogue
    )


def test_execute_transcription_not_sufficient():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create a mock transcription that is not sufficient
    mock_transcription = Mock()
    mock_transcription.is_transcription_sufficient.return_value = False

    # Create a mock DialogueProduct that returns the mock transcription
    mock_dialogue_product = Mock()
    mock_dialogue_product.get_transcription.return_value = mock_transcription

    # Create mock SummarizeDialogueCommandFactory
    mock_summarize_dialogue_command_factory = Mock()

    # Create mock StoreDialoguesCommandFactory
    mock_store_dialogues_command_factory = Mock()

    # Create mock OngoingDialogueRepository
    mock_ongoing_dialogue_repository = Mock()

    # Create mock TimeManager
    mock_time_manager = Mock()

    # Create mock ConfigLoader that returns a specific time advancement
    mock_config_loader = Mock()
    time_advanced_due_to_dialogue = 2
    mock_config_loader.get_time_advanced_due_to_dialogue.return_value = (
        time_advanced_due_to_dialogue
    )

    # Create the EndDialogueCommand instance
    command = EndDialogueCommand(
        playthrough_name=playthrough_name,
        dialogue_product=cast(DialogueProduct, mock_dialogue_product),
        summarize_dialogue_command_factory=mock_summarize_dialogue_command_factory,
        store_dialogues_command_factory=mock_store_dialogues_command_factory,
        ongoing_dialogue_repository=mock_ongoing_dialogue_repository,
        time_manager=mock_time_manager,
        config_loader=mock_config_loader,
    )

    # Act
    command.execute()

    # Assert
    # Ensure that is_transcription_sufficient was called
    mock_transcription.is_transcription_sufficient.assert_called_once()

    # Ensure that summarize_dialogue_command_factory.create_summarize_dialogue_command was not called
    mock_summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_not_called()

    # Ensure that store_dialogues_command_factory.create_command was not called
    mock_store_dialogues_command_factory.create_command.assert_not_called()

    # Ensure that ongoing_dialogue_repository.remove_dialogue was called
    mock_ongoing_dialogue_repository.remove_dialogue.assert_called_once()

    # Ensure that time_manager.advance_time was called with the correct time
    mock_time_manager.advance_time.assert_called_once_with(
        time_advanced_due_to_dialogue
    )


def test_init_with_empty_playthrough_name_raises_value_error():
    # Arrange
    playthrough_name = ""  # Empty string

    # Prepare the other arguments
    mock_dialogue_product = Mock()
    mock_summarize_dialogue_command_factory = Mock()
    mock_store_dialogues_command_factory = Mock()

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        EndDialogueCommand(
            playthrough_name=playthrough_name,
            dialogue_product=cast(DialogueProduct, mock_dialogue_product),
            summarize_dialogue_command_factory=mock_summarize_dialogue_command_factory,
            store_dialogues_command_factory=mock_store_dialogues_command_factory,
        )

    assert "playthrough_name" in str(exc_info.value)


def test_init_with_defaults():
    # Arrange
    playthrough_name = "test_playthrough"

    # Create the necessary mocks
    mock_dialogue_product = Mock()
    mock_summarize_dialogue_command_factory = Mock()
    mock_store_dialogues_command_factory = Mock()

    # Mock the OngoingDialogueRepository, TimeManager, and ConfigLoader classes to check their instantiation
    with patch(
        "src.dialogues.commands.end_dialogue_command.OngoingDialogueRepository"
    ) as MockOngoingDialogueRepository, patch(
        "src.dialogues.commands.end_dialogue_command.TimeManager"
    ) as MockTimeManager, patch(
        "src.dialogues.commands.end_dialogue_command.ConfigLoader"
    ) as MockConfigLoader:
        # Set the mock return values
        mock_ongoing_dialogue_repository_instance = Mock()
        MockOngoingDialogueRepository.return_value = (
            mock_ongoing_dialogue_repository_instance
        )

        mock_time_manager_instance = Mock()
        MockTimeManager.return_value = mock_time_manager_instance

        mock_config_loader_instance = Mock()
        MockConfigLoader.return_value = mock_config_loader_instance

        # Act
        command = EndDialogueCommand(
            playthrough_name=playthrough_name,
            dialogue_product=cast(DialogueProduct, mock_dialogue_product),
            summarize_dialogue_command_factory=mock_summarize_dialogue_command_factory,
            store_dialogues_command_factory=mock_store_dialogues_command_factory,
            ongoing_dialogue_repository=None,
            time_manager=None,
            config_loader=None,
        )

        # Assert
        MockOngoingDialogueRepository.assert_called_once_with(playthrough_name)
        MockTimeManager.assert_called_once_with(playthrough_name)
        MockConfigLoader.assert_called_once()

        # Ensure that the command's attributes are set correctly
        assert (
            command._ongoing_dialogue_repository
            == mock_ongoing_dialogue_repository_instance
        )
        assert command._time_manager == mock_time_manager_instance
        assert command._config_loader == mock_config_loader_instance
