from unittest.mock import Mock

import pytest

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.algorithms.determine_next_speaker_algorithm import (
    DetermineNextSpeakerAlgorithm,
)
from src.dialogues.exceptions import InvalidNextSpeakerError
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)


def test_two_participants_with_player():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )
    participants.add_participant(
        "2",
        "NPC",
        "NPC Description",
        "NPC Personality",
        "NPC Equipment",
        "Player Health",
        "NPC Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    algorithm = DetermineNextSpeakerAlgorithm(
        "playthrough",
        participants=participants,
        transcription=transcription,
        speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
        playthrough_manager=playthrough_manager,
    )

    # Exercise
    result = algorithm.do_algorithm()

    # Verify
    assert result.is_valid()
    assert result.get()["identifier"] == "2"
    assert result.get()["name"] == "NPC"
    assert result.get()["voice_model"] == "NPC Voice Model"


def test_more_than_two_participants():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )
    participants.add_participant(
        "2",
        "NPC1",
        "NPC1 Description",
        "NPC1 Personality",
        "NPC1 Equipment",
        "Player Health",
        "NPC1 Voice Model",
    )
    participants.add_participant(
        "3",
        "NPC2",
        "NPC2 Description",
        "NPC2 Personality",
        "NPC2 Equipment",
        "Player Health",
        "NPC2 Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    # Mock the speech_turn_choice_tool_response_provider_factory
    mock_response_product = Mock(spec=LlmToolResponseProduct)
    mock_response_product.is_valid.return_value = True
    mock_response_product.get.return_value = {
        "identifier": "2",
        "name": "NPC1",
        "voice_model": "NPC1 Voice Model",
    }
    response_provider = Mock()
    response_provider.generate_product.return_value = mock_response_product
    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    speech_turn_choice_tool_response_provider_factory.create_provider.return_value = (
        response_provider
    )

    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    algorithm = DetermineNextSpeakerAlgorithm(
        "playthrough",
        participants=participants,
        transcription=transcription,
        speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
        playthrough_manager=playthrough_manager,
    )

    # Exercise
    result = algorithm.do_algorithm()

    # Verify
    assert result.is_valid()
    assert result.get()["identifier"] == "2"
    assert result.get()["name"] == "NPC1"
    assert result.get()["voice_model"] == "NPC1 Voice Model"


def test_invalid_response_product():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )
    participants.add_participant(
        "2",
        "NPC1",
        "NPC1 Description",
        "NPC1 Personality",
        "NPC1 Equipment",
        "Player Health",
        "NPC1 Voice Model",
    )
    participants.add_participant(
        "3",
        "NPC2",
        "NPC2 Description",
        "NPC2 Personality",
        "NPC2 Equipment",
        "Player Health",
        "NPC2 Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    # Mock the speech_turn_choice_tool_response_provider_factory
    mock_response_product = Mock(spec=LlmToolResponseProduct)
    mock_response_product.is_valid.return_value = False
    mock_response_product.get_error.return_value = "Invalid response"
    response_provider = Mock()
    response_provider.generate_product.return_value = mock_response_product
    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    speech_turn_choice_tool_response_provider_factory.create_provider.return_value = (
        response_provider
    )

    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    algorithm = DetermineNextSpeakerAlgorithm(
        "playthrough",
        participants=participants,
        transcription=transcription,
        speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
        playthrough_manager=playthrough_manager,
    )

    # Exercise & Verify
    with pytest.raises(InvalidNextSpeakerError) as exc_info:
        algorithm.do_algorithm()

    assert str(exc_info.value) == "Invalid response"


def test_next_speaker_is_player():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )
    participants.add_participant(
        "2",
        "NPC1",
        "NPC1 Description",
        "NPC1 Personality",
        "NPC1 Equipment",
        "NPC1 Health",
        "NPC1 Voice Model",
    )
    participants.add_participant(
        "3",
        "NPC2",
        "NPC2 Description",
        "NPC2 Personality",
        "NPC2 Equipment",
        "NPC2 Health",
        "NPC2 Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    # Mock the speech_turn_choice_tool_response_provider_factory
    mock_response_product = Mock(spec=LlmToolResponseProduct)
    mock_response_product.is_valid.return_value = True
    mock_response_product.get.return_value = {
        "identifier": "1",
        "name": "Player",
        "voice_model": "Player Voice Model",
    }
    response_provider = Mock()
    response_provider.generate_product.return_value = mock_response_product
    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    speech_turn_choice_tool_response_provider_factory.create_provider.return_value = (
        response_provider
    )

    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    algorithm = DetermineNextSpeakerAlgorithm(
        "playthrough",
        participants=participants,
        transcription=transcription,
        speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
        playthrough_manager=playthrough_manager,
    )

    # Exercise & Verify
    with pytest.raises(InvalidNextSpeakerError) as exc_info:
        algorithm.do_algorithm()

    assert str(exc_info.value) == "Next speaker cannot be the player."


def test_voice_model_missing_in_response():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )
    participants.add_participant(
        "2",
        "NPC1",
        "NPC1 Description",
        "NPC1 Personality",
        "NPC1 Equipment",
        "NPC1 Health",
        "NPC1 Voice Model",
    )
    participants.add_participant(
        "3",
        "NPC2",
        "NPC2 Description",
        "NPC2 Personality",
        "NPC2 Equipment",
        "NPC2 Health",
        "NPC2 Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    # Mock the speech_turn_choice_tool_response_provider_factory
    mock_response_product = Mock(spec=LlmToolResponseProduct)
    mock_response_product.is_valid.return_value = True
    mock_response_product.get.return_value = {
        "identifier": "2",
        "name": "NPC1",
        # Missing 'voice_model'
    }
    response_provider = Mock()
    response_provider.generate_product.return_value = mock_response_product
    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    speech_turn_choice_tool_response_provider_factory.create_provider.return_value = (
        response_provider
    )

    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    algorithm = DetermineNextSpeakerAlgorithm(
        "playthrough",
        participants=participants,
        transcription=transcription,
        speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
        playthrough_manager=playthrough_manager,
    )

    # Exercise & Verify
    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()

    assert str(exc_info.value) == "voice_model can't be empty."


def test_not_enough_participants():
    # Setup
    participants = Participants()
    participants.add_participant(
        "1",
        "Player",
        "Player Description",
        "Player Personality",
        "Player Equipment",
        "Player Health",
        "Player Voice Model",
    )

    transcription = Transcription()
    transcription.add_speech_turn("Player", "Hello!")

    speech_turn_choice_tool_response_provider_factory = Mock(
        spec=SpeechTurnChoiceToolResponseProviderFactory
    )
    playthrough_manager = Mock(spec=PlaythroughManager)
    playthrough_manager.get_player_identifier.return_value = "1"

    # Exercise & Verify
    with pytest.raises(ValueError) as exc_info:
        DetermineNextSpeakerAlgorithm(
            "playthrough",
            participants=participants,
            transcription=transcription,
            speech_turn_choice_tool_response_provider_factory=speech_turn_choice_tool_response_provider_factory,
            playthrough_manager=playthrough_manager,
        )

    assert "There weren't enough participants for a dialogue." in str(exc_info.value)
