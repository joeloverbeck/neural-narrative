from unittest.mock import MagicMock, patch

import pytest

from src.dialogues.algorithms.handle_dialogue_state_algorithm import (
    HandleDialogueStateAlgorithm,
)
from src.dialogues.products.HandleDialogueStateAlgorithmProduct import (
    HandleDialogueStateAlgorithmProduct,
)


def test_no_dialogue_participants_and_no_ongoing_dialogue_returns_none():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = False

    # Instantiate the algorithm with empty participants and no purpose
    algorithm = HandleDialogueStateAlgorithm(
        playthrough_name="test_playthrough",
        dialogue_participant_identifiers=[],
        purpose=None,
        playthrough_manager=mock_playthrough_manager,
    )

    # Run the algorithm
    result = algorithm.do_algorithm()

    # Assert that the result is a HandleDialogueStateAlgorithmProduct with None data
    assert isinstance(result, HandleDialogueStateAlgorithmProduct)
    assert result.get_data() is None


def test_no_dialogue_participants_with_ongoing_dialogue_loads_participants():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Mock the PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_ongoing_dialogue_path.return_value = (
        "/fake/path/ongoing_dialogue.json"
    )

    # Mock read_json_file to return a fake dialogue file
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        mock_read_json_file.return_value = {
            "participants": ["participant1", "participant2"],
            "purpose": None,
        }

        # Instantiate the algorithm with empty participants and no purpose
        algorithm = HandleDialogueStateAlgorithm(
            playthrough_name="test_playthrough",
            dialogue_participant_identifiers=[],
            purpose="Some purpose",
            playthrough_manager=mock_playthrough_manager,
            path_manager=mock_path_manager,
        )

        # Run the algorithm
        result = algorithm.do_algorithm()

        # Assert that the result contains the participants from the file
        assert isinstance(result, HandleDialogueStateAlgorithmProduct)
        assert result.get_data() == {"participants": ["participant1", "participant2"]}


def test_no_purpose_with_ongoing_dialogue_loads_purpose():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Mock the PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_ongoing_dialogue_path.return_value = (
        "/fake/path/ongoing_dialogue.json"
    )

    # Mock read_json_file to return a fake dialogue file
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        mock_read_json_file.return_value = {
            "purpose": "Discuss project status",
            "participants": [],
        }

        # Instantiate the algorithm with non-empty participants and no purpose
        algorithm = HandleDialogueStateAlgorithm(
            playthrough_name="test_playthrough",
            dialogue_participant_identifiers=["participant1"],
            purpose=None,
            playthrough_manager=mock_playthrough_manager,
            path_manager=mock_path_manager,
        )

        # Run the algorithm
        result = algorithm.do_algorithm()

        # Assert that the result contains the purpose from the file
        assert isinstance(result, HandleDialogueStateAlgorithmProduct)
        assert result.get_data() == {"purpose": "Discuss project status"}


def test_no_participants_no_purpose_with_ongoing_dialogue_loads_both():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Mock the PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_ongoing_dialogue_path.return_value = (
        "/fake/path/ongoing_dialogue.json"
    )

    # Mock read_json_file to return a fake dialogue file
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        mock_read_json_file.return_value = {
            "participants": ["participant1", "participant2"],
            "purpose": "Discuss project status",
        }

        # Instantiate the algorithm with empty participants and no purpose
        algorithm = HandleDialogueStateAlgorithm(
            playthrough_name="test_playthrough",
            dialogue_participant_identifiers=[],
            purpose=None,
            playthrough_manager=mock_playthrough_manager,
            path_manager=mock_path_manager,
        )

        # Run the algorithm
        result = algorithm.do_algorithm()

        # Assert that the result contains both participants and purpose from the file
        assert isinstance(result, HandleDialogueStateAlgorithmProduct)
        assert result.get_data() == {
            "participants": ["participant1", "participant2"],
            "purpose": "Discuss project status",
        }


def test_participants_and_purpose_provided_do_not_load_from_file():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Instantiate the algorithm with participants and purpose
    algorithm = HandleDialogueStateAlgorithm(
        playthrough_name="test_playthrough",
        dialogue_participant_identifiers=["participant1"],
        purpose="Discuss project status",
        playthrough_manager=mock_playthrough_manager,
    )

    # Mock read_json_file to check if it is not called
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        algorithm.do_algorithm()
        # Assert that read_json_file was not called
        mock_read_json_file.assert_not_called()


def test_ongoing_dialogue_file_missing_participants():
    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Mock PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_ongoing_dialogue_path.return_value = (
        "/fake/path/ongoing_dialogue.json"
    )

    # Mock read_json_file to return dialogue without 'participants'
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        mock_read_json_file.return_value = {
            "purpose": "Discuss project status",
            "participants": [],
        }

        # Instantiate the algorithm
        algorithm = HandleDialogueStateAlgorithm(
            playthrough_name="test_playthrough",
            dialogue_participant_identifiers=[],
            purpose=None,
            playthrough_manager=mock_playthrough_manager,
            path_manager=mock_path_manager,
        )

        # Run algorithm
        result = algorithm.do_algorithm()

        # Assert participants is None
        assert result.get_data() == {
            "participants": [],
            "purpose": "Discuss project status",
        }


def test_ongoing_dialogue_file_missing_purpose():
    # Similar to the previous test but missing 'purpose'
    # ...

    # Mock the PlaythroughManager
    mock_playthrough_manager = MagicMock()
    mock_playthrough_manager.has_ongoing_dialogue.return_value = True

    # Mock PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_ongoing_dialogue_path.return_value = (
        "/fake/path/ongoing_dialogue.json"
    )

    # Mock read_json_file to return dialogue without 'purpose'
    with patch(
        "src.dialogues.algorithms.handle_dialogue_state_algorithm.read_json_file"
    ) as mock_read_json_file:
        mock_read_json_file.return_value = {
            "participants": ["participant1", "participant2"],
            "purpose": None,
        }

        # Instantiate the algorithm
        algorithm = HandleDialogueStateAlgorithm(
            playthrough_name="test_playthrough",
            dialogue_participant_identifiers=[],
            purpose=None,
            playthrough_manager=mock_playthrough_manager,
            path_manager=mock_path_manager,
        )

        # Run algorithm
        result = algorithm.do_algorithm()

        # Assert purpose is None
        assert result.get_data() == {
            "participants": ["participant1", "participant2"],
            "purpose": None,
        }


def test_empty_playthrough_name_raises_exception():
    with pytest.raises(ValueError):
        HandleDialogueStateAlgorithm(
            playthrough_name="",
            dialogue_participant_identifiers=[],
            purpose=None,
        )
