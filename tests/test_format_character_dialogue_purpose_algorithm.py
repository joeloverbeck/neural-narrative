# test_format_character_dialogue_purpose_algorithm.py

from unittest.mock import Mock, patch

import pytest

from src.dialogues.algorithms.format_character_dialogue_purpose_algorithm import (
    FormatCharacterDialoguePurposeAlgorithm,
)
from src.filesystem.path_manager import PathManager


# Fixture to mock validate_non_empty_string
@pytest.fixture
def mock_validate_non_empty_string():
    with patch(
        "src.dialogues.algorithms.format_character_dialogue_purpose_algorithm.validate_non_empty_string"
    ) as mock_validator:
        yield mock_validator


# Fixture to mock PathManager
@pytest.fixture
def mock_path_manager():
    with patch(
        "src.dialogues.algorithms.format_character_dialogue_purpose_algorithm.PathManager"
    ) as MockPathManager:
        instance = MockPathManager.return_value
        instance.get_purpose_path.return_value = "/fake/path/purpose.txt"
        yield instance


# Fixture to mock read_file_if_exists
@pytest.fixture
def mock_read_file_if_exists():
    with patch(
        "src.dialogues.algorithms.format_character_dialogue_purpose_algorithm.read_file_if_exists"
    ) as mock_reader:
        yield mock_reader


def test_init_valid_parameters(mock_validate_non_empty_string, mock_path_manager):
    # Arrange
    playthrough_name = "Playthrough1"
    character_identifier = "char_001"
    character_name = "Alice"

    # Act
    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
    )

    # Assert
    mock_validate_non_empty_string.assert_any_call(playthrough_name, "playthrough_name")
    mock_validate_non_empty_string.assert_any_call(
        character_identifier, "character_identifier"
    )
    mock_validate_non_empty_string.assert_any_call(character_name, "character_name")
    mock_path_manager.get_purpose_path.assert_not_called()  # Initialization shouldn't call get_purpose_path
    assert algo._playthrough_name == playthrough_name
    assert algo._character_identifier == character_identifier
    assert algo._character_name == character_name
    assert algo._path_manager == mock_path_manager


def test_do_algorithm_purpose_exists(mock_path_manager, mock_read_file_if_exists):
    # Arrange
    playthrough_name = "Playthrough1"
    character_identifier = "char_001"
    character_name = "Alice"
    purpose_content = "Seek the hidden treasure."

    mock_read_file_if_exists.return_value = purpose_content

    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
        path_manager=mock_path_manager,
    )

    # Act
    result = algo.do_algorithm()

    # Assert
    mock_path_manager.get_purpose_path.assert_called_once_with(
        playthrough_name, character_identifier, character_name
    )
    mock_read_file_if_exists.assert_called_once_with("/fake/path/purpose.txt")
    expected_output = "Alice's Dialogue Purpose: Seek the hidden treasure."
    assert result == expected_output


def test_do_algorithm_purpose_not_exists(mock_path_manager, mock_read_file_if_exists):
    # Arrange
    playthrough_name = "Playthrough1"
    character_identifier = "char_002"
    character_name = "Bob"

    mock_read_file_if_exists.return_value = None  # File does not exist

    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
        path_manager=mock_path_manager,
    )

    # Act
    result = algo.do_algorithm()

    # Assert
    mock_path_manager.get_purpose_path.assert_called_once_with(
        playthrough_name, character_identifier, character_name
    )
    mock_read_file_if_exists.assert_called_once_with("/fake/path/purpose.txt")
    assert result == ""


def test_do_algorithm_purpose_empty_content(
    mock_path_manager, mock_read_file_if_exists
):
    # Arrange
    playthrough_name = "Playthrough2"
    character_identifier = "char_003"
    character_name = "Charlie"

    mock_read_file_if_exists.return_value = ""  # File exists but is empty

    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
        path_manager=mock_path_manager,
    )

    # Act
    result = algo.do_algorithm()

    # Assert
    mock_path_manager.get_purpose_path.assert_called_once_with(
        playthrough_name, character_identifier, character_name
    )
    mock_read_file_if_exists.assert_called_once_with("/fake/path/purpose.txt")
    assert result == ""


def test_init_with_custom_path_manager(mock_validate_non_empty_string):
    # Arrange
    playthrough_name = "Playthrough3"
    character_identifier = "char_004"
    character_name = "Diana"
    custom_path_manager = Mock(spec=PathManager)

    # Act
    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
        path_manager=custom_path_manager,
    )

    # Assert
    mock_validate_non_empty_string.assert_any_call(playthrough_name, "playthrough_name")
    mock_validate_non_empty_string.assert_any_call(
        character_identifier, "character_identifier"
    )
    mock_validate_non_empty_string.assert_any_call(character_name, "character_name")
    assert algo._path_manager == custom_path_manager


def test_do_algorithm_with_custom_path_manager(mock_read_file_if_exists):
    # Arrange
    playthrough_name = "Playthrough4"
    character_identifier = "char_005"
    character_name = "Eve"
    purpose_content = "Protect the realm."

    custom_path_manager = Mock(spec=PathManager)
    custom_path_manager.get_purpose_path.return_value = "/custom/path/purpose_eve.txt"
    mock_read_file_if_exists.return_value = purpose_content

    algo = FormatCharacterDialoguePurposeAlgorithm(
        playthrough_name=playthrough_name,
        character_identifier=character_identifier,
        character_name=character_name,
        path_manager=custom_path_manager,
    )

    # Act
    result = algo.do_algorithm()

    # Assert
    custom_path_manager.get_purpose_path.assert_called_once_with(
        playthrough_name, character_identifier, character_name
    )
    mock_read_file_if_exists.assert_called_once_with("/custom/path/purpose_eve.txt")
    expected_output = "Eve's Dialogue Purpose: Protect the realm."
    assert result == expected_output
