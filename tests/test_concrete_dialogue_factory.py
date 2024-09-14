import logging
from typing import cast
from unittest.mock import Mock

import pytest

from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy
from src.dialogues.factories.concrete_dialogue_factory import ConcreteDialogueFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_dialogue_product import ConcreteDialogueProduct
from src.dialogues.transcription import Transcription


@pytest.fixture
def setup_factory():
    # Mock dependencies
    mock_strategy = Mock()
    mock_command_factory = Mock()
    mock_speech_data_provider_factory = Mock()

    # Create instance of ConcreteDialogueFactory
    factory = ConcreteDialogueFactory(cast(InvolvePlayerInDialogueStrategy, mock_strategy), mock_command_factory,
                                      mock_speech_data_provider_factory)

    return factory, mock_strategy, mock_command_factory, mock_speech_data_provider_factory


def test_initialization(setup_factory):
    factory, _, _, _ = setup_factory

    assert isinstance(factory._messages_to_llm, MessagesToLlm)
    assert isinstance(factory._transcription, Transcription)
    assert factory._observers == []


def test_attach_detach_observer(setup_factory):
    factory, _, _, _ = setup_factory
    mock_observer = Mock()

    factory.attach(mock_observer)
    assert mock_observer in factory._observers

    factory.detach(mock_observer)
    assert mock_observer not in factory._observers


def test_notify_observers(setup_factory):
    factory, _, _, _ = setup_factory
    mock_observer_1 = Mock()
    mock_observer_2 = Mock()

    factory.attach(mock_observer_1)
    factory.attach(mock_observer_2)

    message = {"message": "test"}
    factory.notify(message)

    mock_observer_1.update.assert_called_once_with(message)
    mock_observer_2.update.assert_called_once_with(message)


def test_process_turn_goodbye(setup_factory):
    factory, mock_strategy, _, _ = setup_factory

    # Mock the player input product to return a goodbye
    mock_player_input_product = Mock()
    mock_player_input_product.is_goodbye.return_value = True
    mock_strategy.do_algorithm.return_value = mock_player_input_product

    result = factory.process_turn()

    assert result is False


def test_process_turn_invalid_speech_data(setup_factory, caplog):
    factory, mock_strategy, mock_command_factory, mock_speech_data_provider_factory = setup_factory

    # Mock the player input product to not return goodbye
    mock_player_input_product = Mock()
    mock_player_input_product.is_goodbye.return_value = False
    mock_strategy.do_algorithm.return_value = mock_player_input_product

    # Mock the command execution
    mock_command = Mock()
    mock_command_factory.create_speech_turn_produce_messages_to_prompt_llm_command.return_value = mock_command

    # Mock the invalid speech data product
    mock_speech_data_product = Mock()
    mock_speech_data_product.is_valid.return_value = False
    mock_speech_data_product.get_error.return_value = "Error message"
    mock_speech_data_provider_factory.create_llm_speech_data_provider.return_value.create_speech_data.return_value = mock_speech_data_product

    with caplog.at_level(logging.ERROR):
        result = factory.process_turn()

    assert result is False
    assert "Failed to produce speech data: Error message" in caplog.text


def test_process_turn_success(setup_factory):
    factory, mock_strategy, mock_command_factory, mock_speech_data_provider_factory = setup_factory

    # Mock the player input product to not return goodbye
    mock_player_input_product = Mock()
    mock_player_input_product.is_goodbye.return_value = False
    mock_strategy.do_algorithm.return_value = mock_player_input_product

    # Mock the command execution
    mock_command = Mock()
    mock_command_factory.create_speech_turn_produce_messages_to_prompt_llm_command.return_value = mock_command

    # Mock the valid speech data product
    mock_speech_data_product = Mock()
    mock_speech_data_product.is_valid.return_value = True
    mock_speech_data_product.get.return_value = {
        "name": "NPC",
        "narration_text": "Narration",
        "speech": "Hello"
    }
    mock_speech_data_provider_factory.create_llm_speech_data_provider.return_value.create_speech_data.return_value = mock_speech_data_product

    result = factory.process_turn()

    assert result is True
    assert factory._transcription.get() == ["NPC: *Narration* Hello"]


def test_create_dialogue(setup_factory):
    factory, mock_strategy, _, _ = setup_factory

    # Mock process_turn to return True once, then False
    factory.process_turn = Mock(side_effect=[True, True, False])

    result = factory.create_dialogue()

    assert isinstance(result, ConcreteDialogueProduct)
    assert factory.process_turn.call_count == 3
