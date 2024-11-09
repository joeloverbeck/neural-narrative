# test_get_participant_characters_other_than_player_algorithm.py

from unittest.mock import Mock, patch

import pytest

# Assume the following import path; adjust it based on your project structure
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.algorithms.get_participant_characters_other_than_player_algorithm import (
    GetParticipantCharactersOtherThanPlayerAlgorithm,
)


# Fixtures for common setup
@pytest.fixture
def valid_playthrough_name():
    return "TestPlaythrough"


@pytest.fixture
def valid_dialogue_participants():
    return ["participant1", "participant2", "participant3"]


@pytest.fixture
def mock_playthrough_manager():
    mock = Mock(spec=PlaythroughManager)
    mock.get_player_identifier.return_value = "player1"
    return mock


@pytest.fixture
def mock_characters_manager():
    mock = Mock(spec=CharactersManager)
    mock.get_characters.return_value = [
        Mock(spec=Character, identifier="participant1"),
        Mock(spec=Character, identifier="participant2"),
    ]
    return mock


# Test Initialization with Valid Inputs
def test_init_valid_inputs(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=valid_dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    assert algorithm._dialogue_participants == valid_dialogue_participants
    assert algorithm._playthrough_manager is mock_playthrough_manager
    assert algorithm._characters_manager is mock_characters_manager


# Test Initialization with Empty Playthrough Name
def test_init_empty_playthrough_name(valid_dialogue_participants):
    with pytest.raises(ValueError) as exc_info:
        GetParticipantCharactersOtherThanPlayerAlgorithm(
            playthrough_name="",
            dialogue_participants=valid_dialogue_participants,
        )
    assert "playthrough_name" in str(exc_info.value)


# Test Initialization with Invalid Dialogue Participants (Not a List)
def test_init_invalid_dialogue_participants_not_list(valid_playthrough_name):
    with pytest.raises(TypeError) as exc_info:
        GetParticipantCharactersOtherThanPlayerAlgorithm(
            playthrough_name=valid_playthrough_name,
            dialogue_participants="not_a_list",  # noqa
        )
    assert "The passed value is not" in str(exc_info.value)


# Test Initialization with Invalid Dialogue Participants (List with Non-Strings)
def test_init_invalid_dialogue_participants_non_strings(valid_playthrough_name):
    with pytest.raises(TypeError) as exc_info:
        GetParticipantCharactersOtherThanPlayerAlgorithm(
            playthrough_name=valid_playthrough_name,
            dialogue_participants=["participant1", 123, "participant3"],
        )
    assert "The passed list contains at least" in str(exc_info.value)


# Test Initialization Without Providing PlaythroughManager and CharactersManager
@patch(
    "src.dialogues.algorithms.get_participant_characters_other_than_player_algorithm.PlaythroughManager"
)
@patch(
    "src.dialogues.algorithms.get_participant_characters_other_than_player_algorithm.CharactersManager"
)
def test_init_without_managers(
    mock_characters_manager_class,
    mock_playthrough_manager_class,
    valid_playthrough_name,
    valid_dialogue_participants,
):
    # Configure the mocks
    mock_playthrough_manager_instance = Mock(spec=PlaythroughManager)
    mock_playthrough_manager_class.return_value = mock_playthrough_manager_instance

    mock_characters_manager_instance = Mock(spec=CharactersManager)
    mock_characters_manager_class.return_value = mock_characters_manager_instance

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=valid_dialogue_participants,
    )

    mock_playthrough_manager_class.assert_called_once_with(valid_playthrough_name)
    mock_characters_manager_class.assert_called_once_with(valid_playthrough_name)
    assert algorithm._playthrough_manager is mock_playthrough_manager_instance
    assert algorithm._characters_manager is mock_characters_manager_instance


# Test Initialization With Provided PlaythroughManager and CharactersManager
def test_init_with_provided_managers(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=valid_dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    assert algorithm._playthrough_manager is mock_playthrough_manager
    assert algorithm._characters_manager is mock_characters_manager


# Test do_algorithm with Participants Excluding Player
def test_do_algorithm_excludes_player(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    # Assume 'player1' is the player identifier
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1", "participant1", "participant2"]
    expected_identifiers = ["participant1", "participant2"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(expected_identifiers)
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm When All Participants Are Player
def test_do_algorithm_all_participants_are_player(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1", "player1", "player1"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with([])
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm with Empty Dialogue Participants
def test_do_algorithm_empty_dialogue_participants(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = []

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with([])
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm When PlaythroughManager Raises Exception
def test_do_algorithm_playthrough_manager_exception(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.side_effect = Exception(
        "Playthrough error"
    )

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=valid_dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()

    assert "Playthrough error" in str(exc_info.value)
    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_not_called()


# Test do_algorithm When CharactersManager Raises Exception
def test_do_algorithm_characters_manager_exception(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    mock_characters_manager.get_characters.side_effect = Exception("Characters error")
    dialogue_participants = ["player1", "participant1", "participant2"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    with pytest.raises(Exception) as exc_info:
        algorithm.do_algorithm()

    assert "Characters error" in str(exc_info.value)
    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(
        ["participant1", "participant2"]
    )


# Test do_algorithm with Duplicate Participants
def test_do_algorithm_with_duplicate_participants(
    valid_playthrough_name,
    valid_dialogue_participants,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1", "participant1", "participant1", "participant2"]
    expected_identifiers = ["participant1", "participant1", "participant2"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(expected_identifiers)
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm Case Sensitivity in Excluding Player
def test_do_algorithm_case_sensitivity(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "Player1"
    dialogue_participants = ["player1", "Player1", "PARTICIPANT1"]
    expected_identifiers = ["player1", "PARTICIPANT1"]  # Assuming case-sensitive

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(expected_identifiers)
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm When Dialogue Participants Contain Only Player Identifier
def test_do_algorithm_only_player_identifier(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with([])
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm with Large Number of Participants
def test_do_algorithm_large_number_of_participants(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1"] + [f"participant{i}" for i in range(100)]
    expected_identifiers = [f"participant{i}" for i in range(100)]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(expected_identifiers)
    assert result == mock_characters_manager.get_characters.return_value


# Additional Tests for Edge Cases


# Test do_algorithm with None as dialogue_participants (Should Fail at Initialization)
def test_init_dialogue_participants_none(valid_playthrough_name):
    with pytest.raises(TypeError) as exc_info:
        GetParticipantCharactersOtherThanPlayerAlgorithm(
            playthrough_name=valid_playthrough_name,
            dialogue_participants=None,  # noqa
        )
    assert "passed value is not a list" in str(exc_info.value)


# Test do_algorithm with Non-Unique Participant Identifiers
def test_do_algorithm_non_unique_participants(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1", "participant1", "participant2", "participant1"]
    expected_identifiers = ["participant1", "participant2", "participant1"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(expected_identifiers)
    assert result == mock_characters_manager.get_characters.return_value


# Test do_algorithm when dialogue_participants contains player identifier multiple times
def test_do_algorithm_multiple_player_identifiers(
    valid_playthrough_name,
    mock_playthrough_manager,
    mock_characters_manager,
):
    mock_playthrough_manager.get_player_identifier.return_value = "player1"
    dialogue_participants = ["player1", "participant1", "player1", "participant2"]

    algorithm = GetParticipantCharactersOtherThanPlayerAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants=dialogue_participants,
        playthrough_manager=mock_playthrough_manager,
        characters_manager=mock_characters_manager,
    )

    result = algorithm.do_algorithm()

    mock_playthrough_manager.get_player_identifier.assert_called_once()
    mock_characters_manager.get_characters.assert_called_once_with(
        ["participant1", "participant2"]
    )
    assert result == mock_characters_manager.get_characters.return_value
