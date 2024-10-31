from unittest.mock import Mock, patch

import pytest

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.algorithms.extract_identifiers_from_participants_data_algorithm import (
    ExtractIdentifiersFromParticipantsDataAlgorithm,
)


# Fixtures for common setup
@pytest.fixture
def mock_playthrough_manager():
    mock = Mock(spec=PlaythroughManager)
    mock.get_player_identifier.return_value = "player_1"
    return mock


@pytest.fixture
def valid_playthrough_name():
    return "test_playthrough"


@pytest.fixture
def dialogue_participants_identifiers():
    return ["participant_1", "participant_2"]


@pytest.fixture
def empty_dialogue_participants_identifiers():
    return []


@pytest.fixture
def sample_data():
    return {
        "participants": {
            "player_1": "Player One",
            "participant_1": "Participant One",
            "participant_2": "Participant Two",
        }
    }


# Initialization Tests
def test_initialization_with_valid_inputs(
    valid_playthrough_name, dialogue_participants_identifiers, mock_playthrough_manager
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    assert (
        algorithm._dialogue_participants_identifiers
        == dialogue_participants_identifiers
    )
    assert algorithm._playthrough_manager == mock_playthrough_manager


def test_initialization_without_playthrough_manager(
    valid_playthrough_name, dialogue_participants_identifiers
):
    with patch(
        "src.dialogues.algorithms.extract_identifiers_from_participants_data_algorithm.PlaythroughManager"
    ) as MockPlaythroughManager:
        mock_instance = Mock(spec=PlaythroughManager)
        MockPlaythroughManager.return_value = mock_instance

        algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
            playthrough_name=valid_playthrough_name,
            dialogue_participants_identifiers=dialogue_participants_identifiers,
            playthrough_manager=None,
        )

        MockPlaythroughManager.assert_called_once_with(valid_playthrough_name)
        assert algorithm._playthrough_manager == mock_instance


def test_initialization_with_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        ExtractIdentifiersFromParticipantsDataAlgorithm(
            playthrough_name="",
            dialogue_participants_identifiers=["participant_1"],
            playthrough_manager=None,
        )
    assert "playthrough_name" in str(exc_info.value)


# `do_algorithm` Method Tests
def test_do_algorithm_with_non_empty_dialogue_participants(
    valid_playthrough_name,
    dialogue_participants_identifiers,
    sample_data,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    result = algorithm.do_algorithm(sample_data.copy())

    assert result["participants"] == dialogue_participants_identifiers
    mock_playthrough_manager.get_player_identifier.assert_not_called()


def test_do_algorithm_with_empty_dialogue_participants_and_valid_data(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    sample_data,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    result = algorithm.do_algorithm(sample_data.copy())

    expected_participants = ["participant_1", "participant_2"]  # Excludes 'player_1'
    assert result["participants"] == expected_participants
    mock_playthrough_manager.get_player_identifier.assert_called_once()


def test_do_algorithm_with_empty_dialogue_participants_and_no_participants_key(
    valid_playthrough_name, empty_dialogue_participants_identifiers
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=None,
    )

    data = {}
    result = algorithm.do_algorithm(data.copy())

    assert result["participants"] == empty_dialogue_participants_identifiers


def test_do_algorithm_with_empty_dialogue_participants_and_empty_participants(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    data = {"participants": {}}
    result = algorithm.do_algorithm(data.copy())

    assert result["participants"] == empty_dialogue_participants_identifiers
    mock_playthrough_manager.get_player_identifier.assert_called_once()


def test_do_algorithm_with_only_player_identifier(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    data = {"participants": {"player_1": "Player One"}}
    result = algorithm.do_algorithm(data.copy())

    assert result["participants"] == empty_dialogue_participants_identifiers
    mock_playthrough_manager.get_player_identifier.assert_called_once()


def test_do_algorithm_does_not_modify_original_dialogue_participants(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    sample_data,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers.copy(),
        playthrough_manager=mock_playthrough_manager,
    )

    data = sample_data.copy()
    result = algorithm.do_algorithm(data)

    # Ensure original list is not modified outside the class
    assert empty_dialogue_participants_identifiers == []
    expected_participants = ["participant_1", "participant_2"]
    assert result["participants"] == expected_participants


def test_do_algorithm_with_empty_data_and_empty_dialogue_participants(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    data = {}
    result = algorithm.do_algorithm(data.copy())

    assert result["participants"] == empty_dialogue_participants_identifiers
    mock_playthrough_manager.get_player_identifier.assert_not_called()


def test_do_algorithm_with_none_data(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    with pytest.raises(TypeError):
        # Since data is None, accessing data.get will raise AttributeError
        algorithm.do_algorithm(None)  # noqa


def test_do_algorithm_with_non_string_playthrough_name():
    with pytest.raises(TypeError):
        ExtractIdentifiersFromParticipantsDataAlgorithm(
            playthrough_name=123,  # noqa
            dialogue_participants_identifiers=["participant_1"],
            playthrough_manager=None,
        )


def test_do_algorithm_with_non_dict_data(
    valid_playthrough_name,
    empty_dialogue_participants_identifiers,
    mock_playthrough_manager,
):
    algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=empty_dialogue_participants_identifiers,
        playthrough_manager=mock_playthrough_manager,
    )

    data = ["not", "a", "dict"]
    with pytest.raises(AttributeError):
        # Since data is a list, accessing data.get will raise AttributeError
        algorithm.do_algorithm(data)  # noqa


# Mocking validate_non_empty_string
@patch(
    "src.dialogues.algorithms.extract_identifiers_from_participants_data_algorithm.validate_non_empty_string"
)
def test_initialization_calls_validate_non_empty_string(
    mock_validate, valid_playthrough_name, dialogue_participants_identifiers
):
    ExtractIdentifiersFromParticipantsDataAlgorithm(
        playthrough_name=valid_playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        playthrough_manager=None,
    )

    mock_validate.assert_called_once_with(valid_playthrough_name, "playthrough_name")
