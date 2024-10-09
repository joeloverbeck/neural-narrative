from unittest.mock import MagicMock

import pytest

from src.dialogues.participants import Participants
from src.dialogues.strategies.prevent_llm_from_choosing_player_as_next_speaker_strategy import (
    PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
)
from src.playthrough_manager import PlaythroughManager


def test_prevent_llm_replaces_player_identifier():
    # Mock the PlaythroughManager to return a specific player identifier
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with the player and other characters
    participants = Participants()
    participants.add_participant(
        identifier=player_identifier,
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="3",
        name="Merchant",
        description="A shrewd merchant",
        personality="Greedy",
        equipment="Bag of coins",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player
    function_call_arguments = {
        "identifier": player_identifier,
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the player's identifier has been replaced
    assert updated_arguments["identifier"] != player_identifier
    # Assert that the new identifier is one of the other participants
    assert updated_arguments["identifier"] in ["2", "3"]
    # Assert that the name has been updated accordingly
    assert (
        updated_arguments["name"]
        == participants.get()[updated_arguments["identifier"]]["name"]
    )
    # Assert that the reason has been updated
    assert (
        updated_arguments["reason"]
        == "The LLM incorrectly chose the player as the next speaking choice."
    )


def test_prevent_llm_does_not_change_non_player_identifier():
    # Mock the PlaythroughManager
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants
    participants = Participants()
    participants.add_participant(
        identifier=player_identifier,
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM correctly chooses a non-player participant
    function_call_arguments = {
        "identifier": "2",
        "name": "Villager",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the identifier remains unchanged
    assert updated_arguments["identifier"] == "2"
    # Assert that the name remains unchanged
    assert updated_arguments["name"] == "Villager"
    # Assert that the reason remains unchanged
    assert updated_arguments["reason"] == "Chosen by LLM"


def test_prevent_llm_raises_error_with_only_player():
    # Mock the PlaythroughManager
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with only the player
    participants = Participants()
    participants.add_participant(
        identifier=player_identifier,
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player
    function_call_arguments = {
        "identifier": player_identifier,
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Expect a ValueError since there are no other participants
    with pytest.raises(ValueError) as excinfo:
        strategy.prevent_llm_from_choosing_player(function_call_arguments)

    # Assert that the error message is as expected
    assert (
        str(excinfo.value)
        == "There weren't enough participants for the dialogue to begin with: 1"
    )


def test_prevent_llm_replaces_with_only_one_other_participant():
    # Mock the PlaythroughManager
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with the player and one other participant
    participants = Participants()
    participants.add_participant(
        identifier=player_identifier,
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player
    function_call_arguments = {
        "identifier": player_identifier,
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the identifier has been replaced with the only other participant
    assert updated_arguments["identifier"] == "2"
    # Assert that the name has been updated accordingly
    assert updated_arguments["name"] == "Villager"
    # Assert that the reason has been updated
    assert (
        updated_arguments["reason"]
        == "The LLM incorrectly chose the player as the next speaking choice."
    )


def test_prevent_llm_handles_missing_player_in_participants():
    # Mock the PlaythroughManager with a player identifier not in participants
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants without the player
    participants = Participants()
    participants.add_participant(
        identifier="2",
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="3",
        name="Merchant",
        description="A shrewd merchant",
        personality="Greedy",
        equipment="Bag of coins",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM chooses a participant not matching the player
    function_call_arguments = {
        "identifier": "2",
        "name": "Villager",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the identifier remains unchanged
    assert updated_arguments["identifier"] == "2"
    # Assert that the name remains unchanged
    assert updated_arguments["name"] == "Villager"


def test_prevent_llm_no_participants_raises_error():
    # Mock the PlaythroughManager
    player_identifier = "1"
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with no participants
    participants = Participants()

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player
    function_call_arguments = {
        "identifier": player_identifier,
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Expect a ValueError since there are no participants at all
    with pytest.raises(ValueError) as excinfo:
        strategy.prevent_llm_from_choosing_player(function_call_arguments)

    # Assert that the error message indicates no participants
    assert (
        str(excinfo.value)
        == "There weren't enough participants for the dialogue to begin with: 0"
    )


def test_prevent_llm_with_mismatched_identifier_types():
    # Mock the PlaythroughManager with an int identifier
    player_identifier = 1  # int
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with identifiers as strings
    participants = Participants()
    participants.add_participant(
        identifier="1",  # str
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",  # str
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player with a string identifier
    function_call_arguments = {
        "identifier": "1",  # str
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the player's identifier has been replaced
    assert str(updated_arguments["identifier"]) != str(player_identifier)
    # Assert that the new identifier is one of the other participants
    assert updated_arguments["identifier"] == "2"
    # Assert that the name has been updated accordingly
    assert (
        updated_arguments["name"]
        == participants.get()[updated_arguments["identifier"]]["name"]
    )
    # Assert that the reason has been updated
    assert (
        updated_arguments["reason"]
        == "The LLM incorrectly chose the player as the next speaking choice."
    )


def test_prevent_llm_with_player_identifier_as_stringified_int():
    # Mock the PlaythroughManager with a stringified int identifier
    player_identifier = "1"  # str that looks like an int
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with identifiers as strings
    participants = Participants()
    participants.add_participant(
        identifier="1",  # str
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",  # str
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player with an int identifier
    function_call_arguments = {
        "identifier": 1,  # int
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the player's identifier has been replaced
    assert str(updated_arguments["identifier"]) != player_identifier
    # Assert that the new identifier is one of the other participants
    assert updated_arguments["identifier"] == "2"
    # Assert that the name has been updated accordingly
    assert (
        updated_arguments["name"]
        == participants.get()[updated_arguments["identifier"]]["name"]
    )
    # Assert that the reason has been updated
    assert (
        updated_arguments["reason"]
        == "The LLM incorrectly chose the player as the next speaking choice."
    )


def test_prevent_llm_with_numeric_player_identifier_and_string_function_argument():
    # Mock the PlaythroughManager with a numeric identifier
    player_identifier = 1  # int
    mock_playthrough_manager = MagicMock(spec=PlaythroughManager)
    mock_playthrough_manager.get_player_identifier.return_value = player_identifier

    # Set up Participants with string identifiers
    participants = Participants()
    participants.add_participant(
        identifier="1",  # str
        name="Hero",
        description="The brave adventurer",
        personality="Courageous",
        equipment="Sword and Shield",
        voice_model="default_model",
    )
    participants.add_participant(
        identifier="2",
        name="Villager",
        description="A friendly villager",
        personality="Helpful",
        equipment="Basket of goods",
        voice_model="default_model",
    )

    # Instantiate the strategy class
    strategy = PreventLlmFromChoosingPlayerAsNextSpeakerStrategy(
        playthrough_name="test_playthrough",
        participants=participants,
        playthrough_manager=mock_playthrough_manager,
    )

    # The LLM incorrectly chooses the player with a string identifier
    function_call_arguments = {
        "identifier": "1",  # str
        "name": "Hero",
        "reason": "Chosen by LLM",
    }

    # Before invoking, ensure identifiers are compared correctly
    # If the code does not handle type conversion, this test will reveal the issue

    # Invoke the function
    updated_arguments = strategy.prevent_llm_from_choosing_player(
        function_call_arguments
    )

    # Assert that the player's identifier has been replaced
    assert str(updated_arguments["identifier"]) != str(player_identifier)
    # Assert that the new identifier is one of the other participants
    assert updated_arguments["identifier"] == "2"
    # Assert that the name has been updated accordingly
    assert (
        updated_arguments["name"]
        == participants.get()[updated_arguments["identifier"]]["name"]
    )
    # Assert that the reason has been updated
    assert (
        updated_arguments["reason"]
        == "The LLM incorrectly chose the player as the next speaking choice."
    )
