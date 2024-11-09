from typing import List
from unittest.mock import MagicMock, patch

import pytest

from src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm import (
    LoadDataFromOngoingDialogueAlgorithm,
)
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)


@pytest.fixture
def playthrough_name():
    return "test_playthrough"


@pytest.fixture
def dialogue_participants_identifiers():
    return ["user1", "user2"]


@pytest.fixture
def purpose():
    return "test_purpose"


@pytest.fixture
def mock_repository():
    with patch(
        "src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm.OngoingDialogueRepository"
    ) as MockRepo:
        instance = MockRepo.return_value
        instance.validate_dialogue_is_not_malformed = MagicMock()
        instance.get_participants.return_value = {
            "user1": {"name": "Alice"},
            "user2": {"name": "Bob"},
        }
        instance.get_purpose.return_value = "Loaded Purpose"
        yield instance


def test_do_algorithm_no_ongoing_dialogue(
    playthrough_name: str,
    dialogue_participants_identifiers: List[str],
    purpose: str,
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that when has_ongoing_dialogue is False, do_algorithm returns an empty dictionary.
    """
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        purpose=purpose,
        has_ongoing_dialogue=False,
        ongoing_dialogue_repository=mock_repository,
    )

    result = algorithm.do_algorithm()
    assert result == {}
    mock_repository.validate_dialogue_is_not_malformed.assert_not_called()  # noqa
    mock_repository.get_participants.assert_not_called()  # noqa
    mock_repository.get_purpose.assert_not_called()  # noqa


def test_do_algorithm_ongoing_dialogue_all_data_present(
    playthrough_name: str,
    dialogue_participants_identifiers: List[str],
    purpose: str,
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that when has_ongoing_dialogue is True and both dialogue_participants_identifiers and purpose are provided,
    do_algorithm returns an empty dictionary.
    """
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        purpose=purpose,
        has_ongoing_dialogue=True,
        ongoing_dialogue_repository=mock_repository,
    )

    result = algorithm.do_algorithm()
    assert result == {}
    mock_repository.validate_dialogue_is_not_malformed.assert_not_called()  # noqa
    mock_repository.get_participants.assert_not_called()  # noqa
    mock_repository.get_purpose.assert_not_called()  # noqa


def test_do_algorithm_ongoing_dialogue_missing_participants(
    playthrough_name: str,
    purpose: str,
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that when has_ongoing_dialogue is True and dialogue_participants_identifiers is missing,
    do_algorithm retrieves participants from the repository.
    """
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=None,
        purpose=purpose,
        has_ongoing_dialogue=True,
        ongoing_dialogue_repository=mock_repository,
    )

    result = algorithm.do_algorithm()
    assert result == {
        "participants": {"user1": {"name": "Alice"}, "user2": {"name": "Bob"}}
    }
    mock_repository.validate_dialogue_is_not_malformed.assert_called_once()  # noqa
    mock_repository.get_participants.assert_called_once()  # noqa
    mock_repository.get_purpose.assert_not_called()  # noqa


def test_do_algorithm_ongoing_dialogue_missing_purpose(
    playthrough_name: str,
    dialogue_participants_identifiers: List[str],
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that when has_ongoing_dialogue is True and purpose is missing,
    do_algorithm retrieves purpose from the repository.
    """
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=dialogue_participants_identifiers,
        purpose=None,
        has_ongoing_dialogue=True,
        ongoing_dialogue_repository=mock_repository,
    )

    result = algorithm.do_algorithm()
    assert result == {"purpose": "Loaded Purpose"}
    mock_repository.validate_dialogue_is_not_malformed.assert_called_once()  # noqa
    mock_repository.get_participants.assert_not_called()  # noqa
    mock_repository.get_purpose.assert_called_once()  # noqa


def test_do_algorithm_ongoing_dialogue_missing_both(
    playthrough_name: str,
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that when has_ongoing_dialogue is True and both dialogue_participants_identifiers and purpose are missing,
    do_algorithm retrieves both from the repository.
    """
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=None,
        purpose=None,
        has_ongoing_dialogue=True,
        ongoing_dialogue_repository=mock_repository,
    )

    result = algorithm.do_algorithm()
    expected = {
        "participants": {"user1": {"name": "Alice"}, "user2": {"name": "Bob"}},
        "purpose": "Loaded Purpose",
    }
    assert result == expected
    mock_repository.validate_dialogue_is_not_malformed.assert_called_once()  # noqa
    mock_repository.get_participants.assert_called_once()  # noqa
    mock_repository.get_purpose.assert_called_once()  # noqa


def test_do_algorithm_validate_dialogue_is_malformed(
    playthrough_name: str,
    mock_repository: OngoingDialogueRepository,
):
    """
    Test that do_algorithm raises ValueError when the ongoing dialogue file is malformed.
    """
    mock_repository.validate_dialogue_is_not_malformed.side_effect = ValueError(
        "Malformed dialogue file"
    )

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name=playthrough_name,
        dialogue_participants_identifiers=None,
        purpose=None,
        has_ongoing_dialogue=True,
        ongoing_dialogue_repository=mock_repository,
    )

    with pytest.raises(ValueError, match="Malformed dialogue file"):
        algorithm.do_algorithm()

    mock_repository.validate_dialogue_is_not_malformed.assert_called_once()  # noqa
    mock_repository.get_participants.assert_not_called()  # noqa
    mock_repository.get_purpose.assert_not_called()  # noqa


def test_do_algorithm_repository_instantiated_if_not_provided(
    playthrough_name: str,
    dialogue_participants_identifiers: List[str],
    purpose: str,
):
    """
    Test that OngoingDialogueRepository is instantiated with the correct playthrough_name
    when it is not provided.
    """
    with patch(
        "src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm.OngoingDialogueRepository"
    ) as MockRepo:
        algorithm = LoadDataFromOngoingDialogueAlgorithm(
            playthrough_name=playthrough_name,
            dialogue_participants_identifiers=dialogue_participants_identifiers,
            purpose=purpose,
            has_ongoing_dialogue=True,
            ongoing_dialogue_repository=None,
        )

        # Assuming that do_algorithm is called and repository methods are invoked
        # Mock the methods to prevent actual calls
        mock_instance = MockRepo.return_value
        mock_instance.validate_dialogue_is_not_malformed = MagicMock()
        mock_instance.get_participants.return_value = {}
        mock_instance.get_purpose.return_value = ""

        result = algorithm.do_algorithm()
        assert result == {}

        MockRepo.assert_called_once_with(playthrough_name)
        mock_instance.validate_dialogue_is_not_malformed.assert_not_called()
        mock_instance.get_participants.assert_not_called()
        mock_instance.get_purpose.assert_not_called()


def test_init_with_empty_playthrough_name():
    """
    Test that initializing LoadDataFromOngoingDialogueAlgorithm with an empty playthrough_name
    raises a ValueError.
    """
    with pytest.raises(ValueError, match="playthrough_name"):
        LoadDataFromOngoingDialogueAlgorithm(
            playthrough_name="",
            dialogue_participants_identifiers=None,
            purpose=None,
            has_ongoing_dialogue=True,
            ongoing_dialogue_repository=None,
        )
