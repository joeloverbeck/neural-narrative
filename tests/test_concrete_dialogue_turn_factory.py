from unittest.mock import MagicMock, patch

from src.abstracts.observer import Observer
# Import the ConcreteDialogueTurnFactory and related exceptions
from src.dialogues.factories.concrete_dialogue_turn_factory import (
    ConcreteDialogueTurnFactory,
)


def test_concrete_dialogue_turn_factory_initialization():
    # Mock configurations and dependencies
    dialogue_turn_factory_config = MagicMock()
    dialogue_turn_factory_factories_config = MagicMock()
    dialogue_turn_factory_strategies_config = MagicMock()
    playthrough_manager = MagicMock()

    # Instantiate the class
    factory = ConcreteDialogueTurnFactory(
        dialogue_turn_factory_config,
        dialogue_turn_factory_factories_config,
        dialogue_turn_factory_strategies_config,
        playthrough_manager,
    )

    # Assert that attributes are set correctly
    assert factory._playthrough_name == dialogue_turn_factory_config.playthrough_name
    assert (
        factory._involve_player_in_dialogue_strategy
        == dialogue_turn_factory_strategies_config.involve_player_in_dialogue_strategy
    )
    assert (
        factory._speech_turn_choice_tool_response_provider_factory
        == dialogue_turn_factory_factories_config.speech_turn_choice_tool_response_provider_factory
    )
    assert (
        factory._determine_system_message_for_speech_turn_strategy
        == dialogue_turn_factory_strategies_config.determine_system_message_for_speech_turn_strategy
    )
    assert (
        factory._determine_user_messages_for_speech_turn_strategy_factory
        == dialogue_turn_factory_factories_config.determine_user_messages_for_speech_turn_strategy_factory
    )
    assert factory._messages_to_llm == dialogue_turn_factory_config.messages_to_llm
    assert factory._transcription == dialogue_turn_factory_config.transcription
    assert (
        factory._create_speech_turn_data_command_factory
        == dialogue_turn_factory_factories_config.create_speech_turn_data_command_factory
    )
    assert factory._playthrough_manager == playthrough_manager
    assert factory._observers == []


def test_attach_and_detach_observer():
    observer = MagicMock(spec=Observer)
    factory = ConcreteDialogueTurnFactory(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    # Attach observer
    factory.attach(observer)
    assert observer in factory._observers

    # Detach observer
    factory.detach(observer)
    assert observer not in factory._observers


def test_notify_observers():
    observer1 = MagicMock(spec=Observer)
    observer2 = MagicMock(spec=Observer)
    factory = ConcreteDialogueTurnFactory(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    # Attach observers
    factory.attach(observer1)
    factory.attach(observer2)

    # Notify observers
    message = {"event": "test_event"}
    factory.notify(message)

    # Assert that update was called on both observers
    observer1.update.assert_called_once_with(message)
    observer2.update.assert_called_once_with(message)


@patch(
    "src.dialogues.factories.concrete_dialogue_turn_factory.ConcreteDialogueTurnFactory._create_dialogue_product"
)
@patch(
    "src.dialogues.factories.concrete_dialogue_turn_factory.ConcreteDialogueTurnFactory._get_player_input"
)
def test_process_turn_of_dialogue_player_says_goodbye(
    mock_get_player_input, mock_create_dialogue_product
):
    # Mock player input to simulate goodbye
    player_input_product = MagicMock()
    player_input_product.is_goodbye.return_value = True
    mock_get_player_input.return_value = player_input_product

    # Mock dialogue product
    dialogue_product = MagicMock()
    mock_create_dialogue_product.return_value = dialogue_product

    factory = ConcreteDialogueTurnFactory(
        MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    # Invoke the method
    result = factory.process_turn_of_dialogue()

    # Assertions
    mock_get_player_input.assert_called_once()
    player_input_product.is_goodbye.assert_called_once()
    mock_create_dialogue_product.assert_called_once_with(has_ended=True)
    assert result == dialogue_product
