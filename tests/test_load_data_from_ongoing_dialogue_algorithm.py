from unittest.mock import Mock, patch

import pytest

from src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm import (
    LoadDataFromOngoingDialogueAlgorithm,
)
from src.filesystem.path_manager import PathManager


# Fixtures for common mocks
@pytest.fixture
def mock_path_manager():
    with patch(
        "src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm.PathManager"
    ) as MockPathManager:
        instance = MockPathManager.return_value
        instance.get_ongoing_dialogue_path.return_value = "/fake/path/dialogue.json"
        yield instance


@pytest.fixture
def mock_read_json_file():
    with patch(
        "src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm.read_json_file"
    ) as mock_read:
        yield mock_read


@pytest.fixture
def valid_ongoing_dialogue_file():
    return {
        "participants": ["user1", "user2"],
        "purpose": "Testing dialogue persistence",
    }


# Initialization Tests
def test_init_with_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        LoadDataFromOngoingDialogueAlgorithm(
            playthrough_name="",
            dialogue_participants_identifiers=None,
            purpose=None,
            has_ongoing_dialogue=False,
        )
    assert "playthrough_name" in str(exc_info.value)


def test_init_with_valid_parameters():
    path_manager = Mock(spec=PathManager)
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=["user1"],
        purpose="Test Purpose",
        has_ongoing_dialogue=True,
        path_manager=path_manager,
    )
    assert algorithm._playthrough_name == "TestPlaythrough"
    assert algorithm._dialogue_participants_identifiers == ["user1"]
    assert algorithm._purpose == "Test Purpose"
    assert algorithm._has_ongoing_dialogue is True
    assert algorithm._path_manager is path_manager


def test_init_with_default_path_manager():
    with patch(
        "src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm.PathManager"
    ) as MockPathManager:
        algorithm = LoadDataFromOngoingDialogueAlgorithm(
            playthrough_name="TestPlaythrough",
            dialogue_participants_identifiers=None,
            purpose=None,
            has_ongoing_dialogue=False,
        )
        MockPathManager.assert_called_once()
        assert algorithm._path_manager == MockPathManager.return_value


# do_algorithm Tests
def test_do_algorithm_no_ongoing_dialogue(mock_read_json_file, mock_path_manager):
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=["user1"],
        purpose="Test Purpose",
        has_ongoing_dialogue=False,
        path_manager=mock_path_manager,
    )
    result = algorithm.do_algorithm()
    assert result == {}
    mock_read_json_file.assert_not_called()


def test_do_algorithm_ongoing_dialogue_data_present(
    mock_read_json_file, mock_path_manager, valid_ongoing_dialogue_file
):
    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=["user1"],
        purpose="Test Purpose",
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    result = algorithm.do_algorithm()
    assert result == {}
    mock_read_json_file.assert_not_called()


def test_do_algorithm_missing_participants(
    mock_read_json_file, mock_path_manager, valid_ongoing_dialogue_file
):
    mock_read_json_file.return_value = valid_ongoing_dialogue_file

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=None,
        purpose="Test Purpose",
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    result = algorithm.do_algorithm()
    assert result == {"participants": ["user1", "user2"]}
    mock_read_json_file.assert_called_once_with("/fake/path/dialogue.json")


def test_do_algorithm_missing_purpose(
    mock_read_json_file, mock_path_manager, valid_ongoing_dialogue_file
):
    mock_read_json_file.return_value = valid_ongoing_dialogue_file

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=["user1"],
        purpose=None,
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    result = algorithm.do_algorithm()
    assert result == {"purpose": "Testing dialogue persistence"}
    mock_read_json_file.assert_called_once_with("/fake/path/dialogue.json")


def test_do_algorithm_missing_both(
    mock_read_json_file, mock_path_manager, valid_ongoing_dialogue_file
):
    mock_read_json_file.return_value = valid_ongoing_dialogue_file

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=None,
        purpose=None,
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    result = algorithm.do_algorithm()
    assert result == {
        "participants": ["user1", "user2"],
        "purpose": "Testing dialogue persistence",
    }
    mock_read_json_file.assert_called_once_with("/fake/path/dialogue.json")


def test_do_algorithm_malformed_file_missing_participants(
    mock_read_json_file, mock_path_manager
):
    malformed_file = {"purpose": "Testing dialogue persistence"}
    mock_read_json_file.return_value = malformed_file

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=None,
        purpose="Test Purpose",
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()
    assert "Malformed ongoing dialogue file" in str(exc_info.value)
    mock_read_json_file.assert_called_once_with("/fake/path/dialogue.json")


def test_do_algorithm_malformed_file_missing_purpose(
    mock_read_json_file, mock_path_manager
):
    malformed_file = {"participants": ["user1", "user2"]}
    mock_read_json_file.return_value = malformed_file

    algorithm = LoadDataFromOngoingDialogueAlgorithm(
        playthrough_name="TestPlaythrough",
        dialogue_participants_identifiers=["user1"],
        purpose=None,
        has_ongoing_dialogue=True,
        path_manager=mock_path_manager,
    )
    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()
    assert "Malformed ongoing dialogue file" in str(exc_info.value)
    mock_read_json_file.assert_called_once_with("/fake/path/dialogue.json")
