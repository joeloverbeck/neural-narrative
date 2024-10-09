from unittest.mock import Mock

import pytest

from src.characters.commands.summarize_dialogue_command import SummarizeDialogueCommand
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.factories.dialogue_summary_provider_factory import (
    DialogueSummaryProviderFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


@pytest.fixture
def setup_dependencies():
    # Mocking the transcription
    transcription = Mock(spec=Transcription)

    # Mocking the dialogue summary provider factory and its methods
    dialogue_summary_provider_factory = Mock(spec=DialogueSummaryProviderFactory)
    dialogue_summary_provider = Mock()
    dialogue_summary_provider_factory.create_dialogue_summary_provider.return_value = (
        dialogue_summary_provider
    )

    # Mocking the summary product
    summary_product = Mock()
    dialogue_summary_provider.create_summary.return_value = summary_product

    # Mocking the store character memory factory
    store_character_memory_command_factory = Mock(
        spec=StoreCharacterMemoryCommandFactory
    )
    store_memory_command = Mock()
    store_character_memory_command_factory.create_store_character_memory_command.return_value = (
        store_memory_command
    )

    return {
        "transcription": transcription,
        "dialogue_summary_provider_factory": dialogue_summary_provider_factory,
        "dialogue_summary_provider": dialogue_summary_provider,
        "summary_product": summary_product,
        "store_character_memory_command_factory": store_character_memory_command_factory,
        "store_memory_command": store_memory_command,
    }


def test_no_summary_for_insufficient_transcription(setup_dependencies):
    deps = setup_dependencies

    # Set transcription to be insufficient
    deps["transcription"].is_transcription_sufficient.return_value = False

    participants = Participants()

    participants.add_participant(
        "1", "char_1", "description", "personality", "equipment", "default_model"
    )
    participants.add_participant(
        "2", "char_2", "description", "personality", "equipment", "default_model"
    )

    command = SummarizeDialogueCommand(
        participants=participants,
        transcription=deps["transcription"],
        dialogue_summary_provider_factory=deps["dialogue_summary_provider_factory"],
        store_character_memory_command_factory=deps[
            "store_character_memory_command_factory"
        ],
    )

    command.execute()

    # Ensure that no summary is created if transcription is insufficient
    deps[
        "dialogue_summary_provider_factory"
    ].create_dialogue_summary_provider.assert_not_called()
    deps[
        "store_character_memory_command_factory"
    ].create_store_character_memory_command.assert_not_called()


def test_valid_summary_created_and_memories_stored(setup_dependencies):
    deps = setup_dependencies

    # Set transcription to be sufficient
    deps["transcription"].is_transcription_sufficient.return_value = True

    # Mock the summary product to be valid
    deps["summary_product"].is_valid.return_value = True

    participants = Participants()

    participants.add_participant(
        "1", "char_1", "description", "personality", "equipment", "default_model"
    )
    participants.add_participant(
        "2", "char_2", "description", "personality", "equipment", "default_model"
    )

    command = SummarizeDialogueCommand(
        participants=participants,
        transcription=deps["transcription"],
        dialogue_summary_provider_factory=deps["dialogue_summary_provider_factory"],
        store_character_memory_command_factory=deps[
            "store_character_memory_command_factory"
        ],
    )

    command.execute()

    # Check that summary provider was called
    deps[
        "dialogue_summary_provider_factory"
    ].create_dialogue_summary_provider.assert_called_once_with(deps["transcription"])
    deps["dialogue_summary_provider"].create_summary.assert_called_once()

    # Ensure memories are stored for all participants
    deps[
        "store_character_memory_command_factory"
    ].create_store_character_memory_command.assert_any_call(
        "1", deps["summary_product"].get.return_value
    )
    deps[
        "store_character_memory_command_factory"
    ].create_store_character_memory_command.assert_any_call(
        "2", deps["summary_product"].get.return_value
    )

    # Ensure that the store memory command is executed for each participant
    assert deps["store_memory_command"].execute.call_count == 2


def test_summary_creation_fails(setup_dependencies):
    deps = setup_dependencies

    # Set transcription to be sufficient
    deps["transcription"].is_transcription_sufficient.return_value = True

    # Mock the summary product to be invalid
    deps["summary_product"].is_valid.return_value = False
    deps["summary_product"].get_error.return_value = "Invalid summary"

    participants = Participants()

    participants.add_participant(
        "1", "char_1", "description", "personality", "equipment", "default_model"
    )
    participants.add_participant(
        "2", "char_2", "description", "personality", "equipment", "default_model"
    )

    command = SummarizeDialogueCommand(
        participants=participants,
        transcription=deps["transcription"],
        dialogue_summary_provider_factory=deps["dialogue_summary_provider_factory"],
        store_character_memory_command_factory=deps[
            "store_character_memory_command_factory"
        ],
    )

    with pytest.raises(
        ValueError, match="Failed to create a summary for the dialogue: Invalid summary"
    ):
        command.execute()

    # Ensure that no memory commands are created if summary creation fails
    deps[
        "store_character_memory_command_factory"
    ].create_store_character_memory_command.assert_not_called()
