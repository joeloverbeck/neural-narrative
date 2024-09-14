from unittest.mock import MagicMock

import pytest

from src.dialogues.transcription import Transcription
from src.prompting.providers.speech_turn_tool_response_provider import SpeechTurnChoiceToolResponseProvider


def test_initialization_success():
    # Mocks for the required dependencies
    character_choice_factory_mock = MagicMock()
    llm_content_factory_mock = MagicMock()
    tool_response_parsing_factory_mock = MagicMock()

    # Valid initialization with proper number of participants
    factory = SpeechTurnChoiceToolResponseProvider(
        playthrough_name="test_playthrough",
        participants=["Alice", "Bob"],
        transcription=Transcription(),
        character_choice_dialogue_initial_prompting_messages_provider_factory=character_choice_factory_mock,
        llm_content_provider_factory=llm_content_factory_mock,
        tool_response_parsing_provider_factory=tool_response_parsing_factory_mock
    )

    assert factory._playthrough_name == "test_playthrough"
    assert factory._participants == ["Alice", "Bob"]


def test_initialization_failure():
    # Invalid initialization with less than 2 participants
    with pytest.raises(AssertionError):
        SpeechTurnChoiceToolResponseProvider(
            playthrough_name="test_playthrough",
            participants=["Alice"],  # only one participant
            transcription=Transcription(),
            character_choice_dialogue_initial_prompting_messages_provider_factory=MagicMock(),
            llm_content_provider_factory=MagicMock(),
            tool_response_parsing_provider_factory=MagicMock()
        )


def test_create_llm_response_success():
    # Mock dependencies
    character_choice_factory_mock = MagicMock()
    llm_content_factory_mock = MagicMock()
    tool_response_parsing_factory_mock = MagicMock()

    # Mock gather_participants_data
    gather_participants_data_mock = MagicMock(return_value="mock_participant_data")

    # Mock the LLM response generation and parsing
    character_choice_factory_mock.create_character_choice_dialogue_initial_prompting_messages_provider.return_value.create_initial_prompting_messages.return_value = "mock_initial_messages"
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value.is_valid.return_value = True
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value = MagicMock(
        is_valid=lambda: True)
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.get.return_value = {
        "arguments": {"identifier": "Character1"}
    }
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.is_valid.return_value = True

    factory = SpeechTurnChoiceToolResponseProvider(
        playthrough_name="test_playthrough",
        participants=["Alice", "Bob"],
        transcription=Transcription(),
        character_choice_dialogue_initial_prompting_messages_provider_factory=character_choice_factory_mock,
        llm_content_provider_factory=llm_content_factory_mock,
        tool_response_parsing_provider_factory=tool_response_parsing_factory_mock
    )

    response = factory.create_llm_response()

    assert response.is_valid()
    assert response.get() == {"identifier": "Character1"}


def test_create_llm_response_llm_failure():
    # Mock dependencies
    character_choice_factory_mock = MagicMock()
    llm_content_factory_mock = MagicMock()
    tool_response_parsing_factory_mock = MagicMock()

    # LLM content product returns invalid response
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value.is_valid.return_value = False
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value.get_error.return_value = "LLM error"

    factory = SpeechTurnChoiceToolResponseProvider(
        playthrough_name="test_playthrough",
        participants=["Alice", "Bob"],
        transcription=Transcription(),
        character_choice_dialogue_initial_prompting_messages_provider_factory=character_choice_factory_mock,
        llm_content_provider_factory=llm_content_factory_mock,
        tool_response_parsing_provider_factory=tool_response_parsing_factory_mock
    )

    response = factory.create_llm_response()

    assert not response.is_valid()
    assert response.get_error() == "LLM failed to produce a response: LLM error"


def test_create_llm_response_parsing_failure():
    # Mock dependencies
    character_choice_factory_mock = MagicMock()
    llm_content_factory_mock = MagicMock()
    tool_response_parsing_factory_mock = MagicMock()

    # LLM content product is valid
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value.is_valid.return_value = True

    # Mock the parsing provider to return invalid response
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.is_valid.return_value = False
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.get_error.return_value = "Parsing error"

    factory = SpeechTurnChoiceToolResponseProvider(
        playthrough_name="test_playthrough",
        participants=["Alice", "Bob"],
        transcription=Transcription(),
        character_choice_dialogue_initial_prompting_messages_provider_factory=character_choice_factory_mock,
        llm_content_provider_factory=llm_content_factory_mock,
        tool_response_parsing_provider_factory=tool_response_parsing_factory_mock
    )

    response = factory.create_llm_response()

    assert not response.is_valid()
    assert response.get_error() == "Was unable to parse the tool response from the LLM: Parsing error"


def test_create_llm_response_missing_identifier():
    # Mock dependencies
    character_choice_factory_mock = MagicMock()
    llm_content_factory_mock = MagicMock()
    tool_response_parsing_factory_mock = MagicMock()

    # LLM content product is valid
    llm_content_factory_mock.create_llm_content_provider_factory.return_value.generate_content.return_value.is_valid.return_value = True

    # Mock the parsing provider to return a response without "identifier"
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.is_valid.return_value = True
    tool_response_parsing_factory_mock.create_tool_response_parsing_provider.return_value.parse_tool_response.return_value.get.return_value = {
        "arguments": {}
    }

    factory = SpeechTurnChoiceToolResponseProvider(
        playthrough_name="test_playthrough",
        participants=["Alice", "Bob"],
        transcription=Transcription(),
        character_choice_dialogue_initial_prompting_messages_provider_factory=character_choice_factory_mock,
        llm_content_provider_factory=llm_content_factory_mock,
        tool_response_parsing_provider_factory=tool_response_parsing_factory_mock
    )

    response = factory.create_llm_response()

    assert not response.is_valid()
    assert response.get_error() == "The LLM didn't produce the identifier of the character who ought to speak next: {'arguments': {}}"
