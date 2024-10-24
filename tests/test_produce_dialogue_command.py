from typing import cast
from unittest.mock import Mock

import pytest

# Import the class to be tested
from src.base.constants import TIME_ADVANCED_DUE_TO_DIALOGUE
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactory
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.store_temporary_dialogue_command_factory import (
    StoreTemporaryDialogueCommandFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.time.time_manager import TimeManager


def test_execute_dialogue_not_ended():
    # Arrange
    playthrough_name = "test_playthrough"

    # Mock the dependencies
    dialogue_turn_factory = Mock(spec=DialogueTurnFactory)
    summarize_dialogue_command_factory = Mock(spec=SummarizeDialogueCommandFactory)
    store_dialogues_command_factory = Mock(spec=StoreDialoguesCommandFactory)
    store_temporary_dialogue_command_factory = Mock(
        spec=StoreTemporaryDialogueCommandFactory
    )
    filesystem_manager = Mock(spec=FilesystemManager)
    time_manager = Mock(spec=TimeManager)

    # Mock the dialogue product
    dialogue_product = Mock()
    dialogue_product.has_ended.return_value = False

    # Mock transcription
    transcription = Mock()
    dialogue_product.get_transcription.return_value = transcription

    # Configure the dialogue_turn_factory to return our dialogue_product
    dialogue_turn_factory.process_turn_of_dialogue.return_value = dialogue_product

    # Instantiate the class under test
    command = ProduceDialogueCommand(
        playthrough_name,
        cast(DialogueTurnFactory, dialogue_turn_factory),
        summarize_dialogue_command_factory,
        store_dialogues_command_factory,
        store_temporary_dialogue_command_factory,
        filesystem_manager,
        time_manager,
    )

    # Act
    command.execute()

    # Assert
    dialogue_turn_factory.process_turn_of_dialogue.assert_called_once()
    dialogue_product.has_ended.assert_called_once()
    store_temporary_dialogue_command_factory.create_command.assert_called_once_with(
        transcription
    )
    store_temp_command = (
        store_temporary_dialogue_command_factory.create_command.return_value
    )
    store_temp_command.execute.assert_called_once()
    summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_not_called()
    store_dialogues_command_factory.create_command.assert_not_called()
    filesystem_manager.remove_ongoing_dialogue.assert_not_called()
    time_manager.advance_time.assert_not_called()


def test_execute_dialogue_ended_transcription_sufficient():
    # Arrange
    playthrough_name = "test_playthrough"

    # Mock the dependencies
    dialogue_turn_factory = Mock(spec=DialogueTurnFactory)
    summarize_dialogue_command_factory = Mock(spec=SummarizeDialogueCommandFactory)
    store_dialogues_command_factory = Mock(spec=StoreDialoguesCommandFactory)
    store_temporary_dialogue_command_factory = Mock(
        spec=StoreTemporaryDialogueCommandFactory
    )
    filesystem_manager = Mock(spec=FilesystemManager)
    time_manager = Mock(spec=TimeManager)

    # Mock the dialogue product
    dialogue_product = Mock()
    dialogue_product.has_ended.return_value = True

    # Mock transcription
    transcription = Mock()
    transcription.is_transcription_sufficient.return_value = True
    dialogue_product.get_transcription.return_value = transcription

    # Configure the dialogue_turn_factory to return our dialogue_product
    dialogue_turn_factory.process_turn_of_dialogue.return_value = dialogue_product

    # Instantiate the class under test
    command = ProduceDialogueCommand(
        playthrough_name,
        cast(DialogueTurnFactory, dialogue_turn_factory),
        summarize_dialogue_command_factory,
        store_dialogues_command_factory,
        store_temporary_dialogue_command_factory,
        filesystem_manager,
        time_manager,
    )

    # Act
    command.execute()

    # Assert
    dialogue_turn_factory.process_turn_of_dialogue.assert_called_once()
    dialogue_product.has_ended.assert_called_once()
    transcription.is_transcription_sufficient.assert_called_once()
    summarize_command = (
        summarize_dialogue_command_factory.create_summarize_dialogue_command.return_value
    )
    summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_called_once_with(
        transcription
    )
    summarize_command.execute.assert_called_once()
    store_dialogue_command = store_dialogues_command_factory.create_command.return_value
    store_dialogues_command_factory.create_command.assert_called_once_with(
        transcription
    )
    store_dialogue_command.execute.assert_called_once()
    filesystem_manager.remove_ongoing_dialogue.assert_called_once_with(playthrough_name)
    time_manager.advance_time.assert_called_once_with(TIME_ADVANCED_DUE_TO_DIALOGUE)
    store_temporary_dialogue_command_factory.create_command.assert_not_called()


def test_execute_dialogue_ended_transcription_insufficient():
    # Arrange
    playthrough_name = "test_playthrough"

    # Mock the dependencies
    dialogue_turn_factory = Mock(spec=DialogueTurnFactory)
    summarize_dialogue_command_factory = Mock(spec=SummarizeDialogueCommandFactory)
    store_dialogues_command_factory = Mock(spec=StoreDialoguesCommandFactory)
    store_temporary_dialogue_command_factory = Mock(
        spec=StoreTemporaryDialogueCommandFactory
    )
    filesystem_manager = Mock(spec=FilesystemManager)
    time_manager = Mock(spec=TimeManager)

    # Mock the dialogue product
    dialogue_product = Mock()
    dialogue_product.has_ended.return_value = True

    # Mock transcription
    transcription = Mock()
    transcription.is_transcription_sufficient.return_value = False
    dialogue_product.get_transcription.return_value = transcription

    # Configure the dialogue_turn_factory to return our dialogue_product
    dialogue_turn_factory.process_turn_of_dialogue.return_value = dialogue_product

    # Instantiate the class under test
    command = ProduceDialogueCommand(
        playthrough_name,
        cast(DialogueTurnFactory, dialogue_turn_factory),
        summarize_dialogue_command_factory,
        store_dialogues_command_factory,
        store_temporary_dialogue_command_factory,
        filesystem_manager,
        time_manager,
    )

    # Act
    command.execute()

    # Assert
    dialogue_turn_factory.process_turn_of_dialogue.assert_called_once()
    dialogue_product.has_ended.assert_called_once()
    transcription.is_transcription_sufficient.assert_called_once()
    summarize_dialogue_command_factory.create_summarize_dialogue_command.assert_not_called()
    store_dialogues_command_factory.create_command.assert_not_called()
    filesystem_manager.remove_ongoing_dialogue.assert_called_once_with(playthrough_name)
    time_manager.advance_time.assert_called_once_with(TIME_ADVANCED_DUE_TO_DIALOGUE)
    store_temporary_dialogue_command_factory.create_command.assert_not_called()


def test_init_with_empty_playthrough_name_raises_value_error():
    # Arrange
    playthrough_name = ""

    # Mock the dependencies
    dialogue_turn_factory = Mock()
    summarize_dialogue_command_factory = Mock()
    store_dialogues_command_factory = Mock()
    store_temporary_dialogue_command_factory = Mock()
    filesystem_manager = Mock()
    time_manager = Mock()

    # Act & Assert
    with pytest.raises(ValueError):
        ProduceDialogueCommand(
            playthrough_name,
            cast(DialogueTurnFactory, dialogue_turn_factory),
            summarize_dialogue_command_factory,
            store_dialogues_command_factory,
            store_temporary_dialogue_command_factory,
            filesystem_manager,
            time_manager,
        )
