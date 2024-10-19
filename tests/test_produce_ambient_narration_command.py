from unittest.mock import Mock

import pytest

from src.base.abstracts.command import Command
from src.dialogues.commands.produce_ambient_narration_command import (
    ProduceAmbientNarrationCommand,
)
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.factories.ambient_narration_provider_factory import (
    AmbientNarrationProviderFactory,
)
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import (
    HandlePossibleExistenceOfOngoingConversationCommandFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.observers.web_ambient_narration_observer import (
    WebAmbientNarrationObserver,
)
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription


def test_normal_execution():
    # Arrange
    messages_to_llm = Mock(spec=MessagesToLlm)
    transcription = Mock(spec=Transcription)
    web_ambient_narration_observer = Mock(spec=WebAmbientNarrationObserver)

    # Mock AmbientNarrationProvider and its factory
    ambient_narration_product = Mock(spec=AmbientNarrationProduct)
    ambient_narration_product.is_valid.return_value = True
    ambient_narration_product.get.return_value = "Sample Ambient Narration"

    ambient_narration_provider = Mock()
    ambient_narration_provider.generate_product.return_value = ambient_narration_product

    ambient_narration_provider_factory = Mock(spec=AmbientNarrationProviderFactory)
    ambient_narration_provider_factory.create_provider.return_value = (
        ambient_narration_provider
    )

    # Mock HandlePossibleExistenceOfOngoingConversationCommand and its factory
    handle_possible_existence_command = Mock(spec=Command)
    handle_possible_existence_of_ongoing_conversation_command_factory = Mock(
        spec=HandlePossibleExistenceOfOngoingConversationCommandFactory
    )
    handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command.return_value = (
        handle_possible_existence_command
    )

    store_temporary_dialogue_command = Mock(spec=StoreTemporaryDialogueCommand)

    command = ProduceAmbientNarrationCommand(
        messages_to_llm,
        transcription,
        web_ambient_narration_observer,
        ambient_narration_provider_factory,
        handle_possible_existence_of_ongoing_conversation_command_factory,
        store_temporary_dialogue_command,
    )

    # Act
    command.execute()

    # Assert
    handle_possible_existence_command.execute.assert_called_once()
    ambient_narration_provider_factory.create_provider.assert_called_once_with(
        transcription
    )
    ambient_narration_provider.generate_product.assert_called_once()
    ambient_narration_product.is_valid.assert_called_once()
    web_ambient_narration_observer.update.assert_called_once_with(
        {"alignment": "center", "message_text": "Sample Ambient Narration"}
    )
    messages_to_llm.add_message.assert_called_once_with(
        "assistant", "Sample Ambient Narration", is_guiding_message=False
    )
    store_temporary_dialogue_command.execute.assert_called_once()


def test_invalid_product_raises_value_error():
    # Arrange
    messages_to_llm = Mock(spec=MessagesToLlm)
    transcription = Mock(spec=Transcription)
    web_ambient_narration_observer = Mock(spec=WebAmbientNarrationObserver)

    # Mock AmbientNarrationProvider and its factory
    ambient_narration_product = Mock(spec=AmbientNarrationProduct)
    ambient_narration_product.is_valid.return_value = False
    ambient_narration_product.get_error.return_value = "Error message"

    ambient_narration_provider = Mock()
    ambient_narration_provider.generate_product.return_value = ambient_narration_product

    ambient_narration_provider_factory = Mock(spec=AmbientNarrationProviderFactory)
    ambient_narration_provider_factory.create_provider.return_value = (
        ambient_narration_provider
    )

    # Mock HandlePossibleExistenceOfOngoingConversationCommand and its factory
    handle_possible_existence_command = Mock(spec=Command)
    handle_possible_existence_of_ongoing_conversation_command_factory = Mock(
        spec=HandlePossibleExistenceOfOngoingConversationCommandFactory
    )
    handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command.return_value = (
        handle_possible_existence_command
    )

    store_temporary_dialogue_command = Mock(spec=StoreTemporaryDialogueCommand)

    command = ProduceAmbientNarrationCommand(
        messages_to_llm,
        transcription,
        web_ambient_narration_observer,
        ambient_narration_provider_factory,
        handle_possible_existence_of_ongoing_conversation_command_factory,
        store_temporary_dialogue_command,
    )

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        command.execute()
    assert (
        str(excinfo.value)
        == "Was unable to generate ambient narration. Error: Error message"
    )

    handle_possible_existence_command.execute.assert_called_once()
    ambient_narration_provider_factory.create_provider.assert_called_once_with(
        transcription
    )
    ambient_narration_provider.generate_product.assert_called_once()
    ambient_narration_product.is_valid.assert_called_once()
    ambient_narration_product.get_error.assert_called_once()
    web_ambient_narration_observer.update.assert_not_called()
    messages_to_llm.add_message.assert_not_called()
    store_temporary_dialogue_command.execute.assert_not_called()


def test_handle_possible_existence_command_raises_exception():
    # Arrange
    messages_to_llm = Mock(spec=MessagesToLlm)
    transcription = Mock(spec=Transcription)
    web_ambient_narration_observer = Mock(spec=WebAmbientNarrationObserver)
    ambient_narration_provider_factory = Mock(spec=AmbientNarrationProviderFactory)

    # Mock HandlePossibleExistenceOfOngoingConversationCommand and its factory
    handle_possible_existence_command = Mock(spec=Command)
    handle_possible_existence_command.execute.side_effect = Exception("Test exception")
    handle_possible_existence_of_ongoing_conversation_command_factory = Mock(
        spec=HandlePossibleExistenceOfOngoingConversationCommandFactory
    )
    handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command.return_value = (
        handle_possible_existence_command
    )

    store_temporary_dialogue_command = Mock(spec=StoreTemporaryDialogueCommand)

    command = ProduceAmbientNarrationCommand(
        messages_to_llm,
        transcription,
        web_ambient_narration_observer,
        ambient_narration_provider_factory,
        handle_possible_existence_of_ongoing_conversation_command_factory,
        store_temporary_dialogue_command,
    )

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        command.execute()
    assert str(excinfo.value) == "Test exception"

    handle_possible_existence_command.execute.assert_called_once()
    ambient_narration_provider_factory.create_provider.assert_not_called()
    web_ambient_narration_observer.update.assert_not_called()
    messages_to_llm.add_message.assert_not_called()
    store_temporary_dialogue_command.execute.assert_not_called()


def test_generate_product_raises_exception():
    # Arrange
    messages_to_llm = Mock(spec=MessagesToLlm)
    transcription = Mock(spec=Transcription)
    web_ambient_narration_observer = Mock(spec=WebAmbientNarrationObserver)

    # Mock AmbientNarrationProvider and its factory
    ambient_narration_provider = Mock()
    ambient_narration_provider.generate_product.side_effect = Exception(
        "Generation error"
    )

    ambient_narration_provider_factory = Mock(spec=AmbientNarrationProviderFactory)
    ambient_narration_provider_factory.create_provider.return_value = (
        ambient_narration_provider
    )

    # Mock HandlePossibleExistenceOfOngoingConversationCommand and its factory
    handle_possible_existence_command = Mock(spec=Command)
    handle_possible_existence_of_ongoing_conversation_command_factory = Mock(
        spec=HandlePossibleExistenceOfOngoingConversationCommandFactory
    )
    handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command.return_value = (
        handle_possible_existence_command
    )

    store_temporary_dialogue_command = Mock(spec=StoreTemporaryDialogueCommand)

    command = ProduceAmbientNarrationCommand(
        messages_to_llm,
        transcription,
        web_ambient_narration_observer,
        ambient_narration_provider_factory,
        handle_possible_existence_of_ongoing_conversation_command_factory,
        store_temporary_dialogue_command,
    )

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        command.execute()
    assert str(excinfo.value) == "Generation error"

    handle_possible_existence_command.execute.assert_called_once()
    ambient_narration_provider_factory.create_provider.assert_called_once_with(
        transcription
    )
    ambient_narration_provider.generate_product.assert_called_once()
    web_ambient_narration_observer.update.assert_not_called()
    messages_to_llm.add_message.assert_not_called()
    store_temporary_dialogue_command.execute.assert_not_called()
