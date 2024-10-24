import logging
from typing import cast
from unittest.mock import Mock

import pytest

from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.commands.create_speech_turn_data_command import (
    CreateSpeechTurnDataCommand,
)


# Test case 1: Happy path where everything works as expected
def test_execute_happy_path():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()
    transcription.get.return_value = []

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_1",
        "name": "Character One",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = True
    speech_data_product.get.return_value = {
        "narration_text": "smiles warmly",
        "speech": "Hello there!",
        "name": "Character One",
    }

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    observer = Mock()
    command.attach(observer)

    # Act
    command.execute()

    # Assert
    transcription.add_speech_turn.assert_called_with(
        "Character One", "*smiles warmly* Hello there!"
    )
    observer.update.assert_called_with({"message": "some data"})
    speech_data_product.get_error.assert_not_called()
    message_data_producer_for_speech_turn_strategy.produce_message_data.assert_called_with(
        speech_turn_choice_response, speech_data_product
    )


# Test case 2: Handling invalid speech data
def test_execute_invalid_speech_data():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()
    transcription.get.return_value = []

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_2",
        "name": "Character Two",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = False
    speech_data_product.get_error.return_value = "Some error occurred"
    speech_data_product.get.return_value = {}

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data",
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    observer = Mock()
    command.attach(observer)

    # Act
    command.execute()

    # Assert
    speech_data_product.get_error.assert_called()
    assert speech_data_product.get()["narration_text"] == "Looks confused."
    assert speech_data_product.get()["speech"] == "I don't know what to say."
    transcription.add_speech_turn.assert_called_with(
        "Character Two", "*Looks confused.* I don't know what to say."
    )
    observer.update.assert_called_with({"message": "some data"})


# Test case 3: Handling missing or 'none' narration text
def test_execute_missing_narration_text():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()
    transcription.get.return_value = []

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_3",
        "name": "Character Three",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = True
    speech_data_product.get.return_value = {
        "narration_text": None,
        "speech": "This is my speech.",
        "name": "Character Three",
    }

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    observer = Mock()
    command.attach(observer)

    # Act
    command.execute()

    # Assert
    assert (
        speech_data_product.get()["narration_text"]
        == "Character Three takes a moment to speak."
    )
    transcription.add_speech_turn.assert_called_with(
        "Character Three",
        "*Character Three takes a moment to speak.* This is my speech.",
    )
    observer.update.assert_called_with({"message": "some data"})


# Test case 4: Observer notifications
def test_observer_notification():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_4",
        "name": "Character Four",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = True
    speech_data_product.get.return_value = {
        "narration_text": "nods",
        "speech": "Yes, I agree.",
        "name": "Character Four",
    }

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    observer1 = Mock()
    observer2 = Mock()
    command.attach(observer1)
    command.attach(observer2)

    # Act
    command.execute()

    # Assert
    observer1.update.assert_called_with({"message": "some data"})
    observer2.update.assert_called_with({"message": "some data"})


# Test case 5: Execution without observers
def test_execute_no_observers():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_5",
        "name": "Character Five",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = True
    speech_data_product.get.return_value = {
        "narration_text": "looks around",
        "speech": "Where are we?",
        "name": "Character Five",
    }

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    # Act
    command.execute()

    # Assert
    transcription.add_speech_turn.assert_called_with(
        "Character Five", "*looks around* Where are we?"
    )


# Test case 6: Logging on invalid speech data
def test_logging_on_invalid_speech_data(caplog):
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_6",
        "name": "Character Six",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = False
    speech_data_product.get_error.return_value = "Error generating speech data"
    speech_data_product.get.return_value = {}

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    # Act
    with caplog.at_level(logging.ERROR):
        command.execute()

    # Assert
    assert "Failed to produce speech data: Error generating speech data" in caplog.text


# Test case 7: Logging on missing narration text
def test_logging_on_missing_narration_text(caplog):
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_7",
        "name": "Character Seven",
    }

    speech_data_product = Mock()
    speech_data_product.is_valid.return_value = True
    speech_data_product.get.return_value = {
        "narration_text": None,
        "speech": "I have nothing to say.",
        "name": "Character Seven",
    }

    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.return_value = speech_data_product
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()
    message_data_producer_for_speech_turn_strategy.produce_message_data.return_value = {
        "message": "some data"
    }

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    # Act
    with caplog.at_level(logging.WARNING):
        command.execute()

    # Assert
    assert "Speech turn didn't produce narration text. Content:" in caplog.text


# Test case 9: Exception handling during execution
def test_execute_with_exception():
    # Arrange
    transcription = Mock()
    transcription.add_speech_turn = Mock()

    speech_turn_choice_response = Mock()
    speech_turn_choice_response.get.return_value = {
        "identifier": "character_8",
        "name": "Character Eight",
    }

    # Simulate exception in generate_product
    llm_speech_data_provider_factory = Mock()
    llm_speech_data_provider = Mock()
    llm_speech_data_provider.generate_product.side_effect = Exception(
        "Generation failed"
    )
    llm_speech_data_provider_factory.create_llm_speech_data_provider.return_value = (
        llm_speech_data_provider
    )

    message_data_producer_for_speech_turn_strategy = Mock()

    command = CreateSpeechTurnDataCommand(
        transcription,
        speech_turn_choice_response,
        llm_speech_data_provider_factory,
        cast(
            MessageDataProducerForSpeechTurnStrategy,
            message_data_producer_for_speech_turn_strategy,
        ),
    )

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        command.execute()
    assert "Generation failed" in str(excinfo.value)
