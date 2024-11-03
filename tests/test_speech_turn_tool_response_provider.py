# test_speech_turn_choice_tool_response_provider.py
from typing import cast
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.models.speech_turn_choice import SpeechTurnChoice
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.speech_turn_tool_response_provider import (
    SpeechTurnChoiceToolResponseProvider,
)


def test_init_with_valid_parameters():
    # Arrange
    player_identifier = "1"
    participants = Participants()
    transcription = Transcription()
    character_factory = MagicMock(spec=CharacterFactory)
    produce_tool_response_strategy_factory = MagicMock(
        spec=ProduceToolResponseStrategyFactory
    )
    filesystem_manager = MagicMock(spec=FilesystemManager)

    # Act
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier=player_identifier,
        participants=participants,
        transcription=transcription,
        character_factory=character_factory,
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager=filesystem_manager,
    )

    # Assert
    assert provider._player_identifier == player_identifier
    assert provider._participants == participants
    assert provider._transcription == transcription
    assert provider._character_factory == character_factory
    assert (
        provider._produce_tool_response_strategy_factory
        == produce_tool_response_strategy_factory
    )
    assert provider._filesystem_manager == filesystem_manager


def test_init_with_empty_player_identifier_raises_error():
    # Arrange
    player_identifier = ""
    participants = Participants()
    transcription = Transcription()
    character_factory = MagicMock(spec=CharacterFactory)
    produce_tool_response_strategy_factory = MagicMock(
        spec=ProduceToolResponseStrategyFactory
    )

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        SpeechTurnChoiceToolResponseProvider(
            player_identifier=player_identifier,
            participants=participants,
            transcription=transcription,
            character_factory=character_factory,
            produce_tool_response_strategy_factory=cast(
                ProduceToolResponseStrategyFactory,
                produce_tool_response_strategy_factory,
            ),
        )
    assert "player_identifier" in str(exc_info.value)


def test_get_tool_data_returns_correct_schema():
    # Arrange
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    # Act
    tool_data = provider._get_tool_data(SpeechTurnChoice)

    # Assert
    assert tool_data == SpeechTurnChoice.model_json_schema()


def test_get_user_content_returns_expected_string():
    # Arrange
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    # Act
    user_content = provider.get_user_content()

    # Assert
    expected_content = "Choose who will speak next in this dialogue. Choose only among the allowed participants."
    assert user_content == expected_content


def test_create_product_from_base_model_creates_correct_product():
    # Arrange
    character_factory = MagicMock(spec=CharacterFactory)
    character = MagicMock()
    character.voice_model = "TestVoiceModel"
    character_factory.create_character.return_value = character

    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=character_factory,
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    identifier = 2

    base_model = SpeechTurnChoice(
        identifier=identifier, name="Alice", reason="Because Alice should speak next."
    )

    # Act
    product = provider.create_product_from_base_model(base_model)

    # Assert
    expected_llm_response = {
        "identifier": str(identifier),
        "name": base_model.name,
        "reason": base_model.reason,
        "voice_model": character.voice_model,
    }
    assert product.get() == expected_llm_response
    assert product.is_valid() is True
    assert product.get_error() is None


def test_get_prompt_kwargs_with_player_identifier():
    # Arrange
    participants = Participants()
    participants.add_participant(
        identifier="1",
        name="Player",
        description="A brave adventurer.",
        personality="Bold and daring.",
        equipment="Sword and shield.",
        health="Full health.",
        voice_model="PlayerVoiceModel",
    )
    participants.add_participant(
        identifier="2",
        name="Alice",
        description="A wise mage.",
        personality="Thoughtful and calm.",
        equipment="Magic staff.",
        health="Full health.",
        voice_model="AliceVoiceModel",
    )
    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello there!")
    transcription.add_speech_turn("Alice", "Greetings, traveler.")

    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=participants,
        transcription=transcription,
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    # Act
    prompt_kwargs = provider.get_prompt_kwargs()

    # Assert
    expected_all_participants = (
        "Identifier: 1 / Name: Player\n" "Identifier: 2 / Name: Alice"
    )
    expected_participants_without_player = (
        "Identifier: 2 / Name: Alice / Personality: Thoughtful and calm."
    )
    assert prompt_kwargs["all_participants"] == expected_all_participants
    assert (
        prompt_kwargs["participants_without_player"]
        == expected_participants_without_player
    )
    assert prompt_kwargs["dialogue"] == transcription.get_prettified_transcription()


@patch("src.prompting.providers.base_tool_response_provider.read_file")
def test_generate_product_calls_produce_tool_response(mock_read_file):
    # Arrange
    filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_file.return_value = "Prompt content"
    produce_tool_response_strategy_factory = MagicMock(
        spec=ProduceToolResponseStrategyFactory
    )
    strategy = MagicMock()
    produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
        strategy
    )

    identifier = 2

    strategy.produce_tool_response.return_value = SpeechTurnChoice(
        identifier=identifier, name="Alice", reason="She is the next logical speaker."
    )

    character_factory = MagicMock(spec=CharacterFactory)
    character = MagicMock()
    character.voice_model = "AliceVoiceModel"
    character_factory.create_character.return_value = character

    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=character_factory,
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager=filesystem_manager,
    )

    # Act
    product = provider.generate_product(SpeechTurnChoice)

    # Assert
    assert product.is_valid() is True
    expected_response = {
        "identifier": str(identifier),
        "name": "Alice",
        "reason": "She is the next logical speaker.",
        "voice_model": "AliceVoiceModel",
    }
    assert product.get() == expected_response


def test_create_product_from_base_model_with_invalid_model():
    # Arrange
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    # Create a BaseModel that lacks required fields
    class IncompleteSpeechTurnChoice(BaseModel):
        identifier: int

    base_model = IncompleteSpeechTurnChoice(identifier=2)

    # Act & Assert
    with pytest.raises(AttributeError):
        provider.create_product_from_base_model(base_model)


def test_peep_into_system_content_does_nothing():
    # Arrange
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory,
            MagicMock(spec=ProduceToolResponseStrategyFactory),
        ),
    )

    # Act
    result = provider.peep_into_system_content("Some system content")

    # Assert
    assert result is None  # Method does nothing


@patch("src.prompting.providers.base_tool_response_provider.read_file")
def test_generate_product_with_invalid_tool_response(mock_read_file):
    # Arrange
    filesystem_manager = MagicMock(spec=FilesystemManager)
    mock_read_file.return_value = "Prompt content"
    produce_tool_response_strategy_factory = MagicMock(
        spec=ProduceToolResponseStrategyFactory
    )
    strategy = MagicMock()
    produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
        strategy
    )

    # Simulate invalid tool response
    strategy.produce_tool_response.return_value = None

    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(spec=CharacterFactory),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager=filesystem_manager,
    )

    # Act & Assert
    with pytest.raises(NotImplementedError):
        provider.generate_product(SpeechTurnChoice)


def test_get_formatted_prompt_returns_none():
    # Arrange
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
    )

    # Act
    result = provider.get_formatted_prompt()

    # Assert
    assert result is None  # Should return None as per implementation


@patch("src.prompting.providers.base_tool_response_provider.read_file")
def test_generate_system_content_calls_format_prompt_correctly(mock_read_file):
    # Arrange
    filesystem_manager = MagicMock(spec=FilesystemManager)
    prompt_content = "Prompt template with {placeholder}"
    mock_read_file.return_value = prompt_content
    provider = SpeechTurnChoiceToolResponseProvider(
        player_identifier="1",
        participants=Participants(),
        transcription=Transcription(),
        character_factory=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        filesystem_manager=filesystem_manager,
    )
    provider.get_prompt_kwargs = MagicMock(return_value={"placeholder": "value"})

    # Act
    formatted_prompt = provider.get_formatted_prompt()
    if formatted_prompt is None:
        prompt_file = provider.get_prompt_file()
        prompt_kwargs = provider.get_prompt_kwargs()
        prompt_template = provider._read_prompt_file(prompt_file)
        formatted_prompt = provider._format_prompt(prompt_template, **prompt_kwargs)

    # Assert
    assert formatted_prompt == "Prompt template with value"
