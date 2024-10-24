from unittest.mock import Mock

import pytest

from src.base.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.factories.introduce_player_input_into_dialogue_command_factory import (
    IntroducePlayerInputIntoDialogueCommandFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import (
    ConcreteInvolvePlayerInDialogueStrategy,
)
from src.dialogues.transcription import Transcription


@pytest.fixture
def mock_player_input_factory():
    return Mock(spec=PlayerInputFactory)


@pytest.fixture
def mock_player_input_product():
    return Mock(spec=PlayerInputProduct)


@pytest.fixture
def mock_transcription():
    return Mock(spec=Transcription)


@pytest.fixture
def mock_messages_to_llm():
    return Mock(spec=MessagesToLlm)


@pytest.fixture
def mock_command_factory():
    return Mock(spec=IntroducePlayerInputIntoDialogueCommandFactory)


@pytest.fixture
def mock_observer():
    return Mock(spec=Observer)


@pytest.fixture
def strategy(mock_player_input_factory, mock_command_factory):
    return ConcreteInvolvePlayerInDialogueStrategy(
        player_identifier="player_1",
        player_input_factory=mock_player_input_factory,
        introduce_player_input_into_dialogue_command_factory=mock_command_factory,
    )


def test_initialization(strategy):
    assert strategy._player_identifier == "player_1"
    assert strategy._player_input_factory is not None
    assert strategy._introduce_player_input_into_dialogue_command_factory is not None
    assert strategy._observers == []


def test_attach_observer(strategy, mock_observer):
    strategy.attach(mock_observer)
    assert mock_observer in strategy._observers


def test_detach_observer(strategy, mock_observer):
    strategy.attach(mock_observer)
    strategy.detach(mock_observer)
    assert mock_observer not in strategy._observers


def test_notify_observers(strategy, mock_observer):
    strategy.attach(mock_observer)
    message = {"key": "value"}
    strategy.notify(message)
    mock_observer.update.assert_called_once_with(message)


def test_do_algorithm_goodbye(
    strategy, mock_player_input_factory, mock_player_input_product, mock_transcription
):
    mock_player_input_factory.create_player_input.return_value = (
        mock_player_input_product
    )
    mock_player_input_product.is_goodbye.return_value = True
    result = strategy.do_algorithm(mock_transcription)
    assert result == mock_player_input_product
    mock_player_input_factory.create_player_input.assert_called_once()
    mock_player_input_product.is_goodbye.assert_called_once()


def test_do_algorithm_silent_player(
    strategy, mock_player_input_factory, mock_player_input_product, mock_transcription
):
    mock_player_input_factory.create_player_input.return_value = (
        mock_player_input_product
    )
    mock_player_input_product.is_goodbye.return_value = False
    mock_player_input_product.is_silent.return_value = True
    result = strategy.do_algorithm(mock_transcription)
    assert result == mock_player_input_product
    mock_player_input_factory.create_player_input.assert_called_once()
    mock_player_input_product.is_silent.assert_called_once()


def test_do_algorithm_with_input(
    strategy,
    mock_player_input_factory,
    mock_player_input_product,
    mock_command_factory,
    mock_observer,
    mock_transcription,
):
    mock_player_input_factory.create_player_input.return_value = (
        mock_player_input_product
    )
    mock_player_input_product.is_goodbye.return_value = False
    mock_player_input_product.is_silent.return_value = False
    mock_command = Mock()
    (mock_command_factory.create_command.return_value) = mock_command
    strategy.attach(mock_observer)
    result = strategy.do_algorithm(mock_transcription)
    assert result == mock_player_input_product
    mock_command_factory.create_command.assert_called_once_with(
        mock_player_input_product, mock_transcription
    )
    mock_command.attach.assert_called_once_with(mock_observer)
    mock_command.execute.assert_called_once()
