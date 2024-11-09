# test_get_available_characters_algorithm.py

from unittest.mock import Mock, patch

import pytest

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.algorithms.get_available_characters_algorithm import (
    GetAvailableCharactersAlgorithm,
)


# Define sample Character instances for testing
@pytest.fixture
def character1():
    char = Mock(spec=Character)
    char.identifier = "char_1"
    return char


@pytest.fixture
def character2():
    char = Mock(spec=Character)
    char.identifier = "char_2"
    return char


@pytest.fixture
def character3():
    char = Mock(spec=Character)
    char.identifier = "char_3"
    return char


# Fixture for a mocked CharactersManager
@pytest.fixture
def mock_characters_manager(character1, character2, character3):
    manager = Mock(spec=CharactersManager)
    manager.get_characters_at_current_place_plus_followers.return_value = [
        character1,
        character2,
        character3,
    ]
    return manager


# Test Initialization with valid inputs
def test_init_valid_inputs(mock_characters_manager):
    playthrough_name = "Adventure1"
    character_identifiers = ["char_1", "char_2"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    assert algo._character_identifiers == character_identifiers
    assert algo._characters_manager == mock_characters_manager


# Test Initialization with empty playthrough_name
def test_init_empty_playthrough_name():
    with pytest.raises(ValueError) as exc_info:
        GetAvailableCharactersAlgorithm(
            playthrough_name="", character_identifiers=["char_1"]
        )
    assert "'playthrough_name' must be a non-empty string." in str(exc_info.value)


# Test Initialization with non-string playthrough_name
def test_init_non_string_playthrough_name():
    with pytest.raises(TypeError) as exc_info:
        GetAvailableCharactersAlgorithm(
            playthrough_name=123, character_identifiers=["char_1"]  # Non-string # noqa
        )
    assert "'playthrough_name' should have been a 'str', but was" in str(exc_info.value)
    # Note: There might be a mistake in the original validate_non_empty_string function where
    # type(variable_name) is used instead of type(value). Adjust the test accordingly if needed.


# Test Initialization with character_identifiers not a list
def test_init_character_identifiers_not_list():
    with pytest.raises(TypeError) as exc_info:
        GetAvailableCharactersAlgorithm(
            playthrough_name="Adventure1",
            character_identifiers="char_1",  # Not a list # noqa
        )
    assert "The passed value is not a list" in str(exc_info.value)


# Test Initialization with character_identifiers containing non-strings
def test_init_character_identifiers_with_non_strings():
    with pytest.raises(TypeError) as exc_info:
        GetAvailableCharactersAlgorithm(
            playthrough_name="Adventure1",
            character_identifiers=["char_1", 2, "char_3"],  # Contains non-string
        )
    assert "The passed list contains at least an element that isn't a string" in str(
        exc_info.value
    )


# Test do_algorithm with provided CharactersManager, ensuring filtering works
def test_do_algorithm_filters_characters(
    mock_characters_manager, character1, character2, character3
):
    playthrough_name = "Adventure1"
    character_identifiers = ["char_2"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    # Should exclude character2
    assert available_characters == [character1, character3]
    mock_characters_manager.get_characters_at_current_place_plus_followers.assert_called_once()


# Test do_algorithm without providing CharactersManager, ensuring it instantiates CharactersManager
@patch("src.dialogues.algorithms.get_available_characters_algorithm.CharactersManager")
def test_do_algorithm_without_characters_manager(
    mock_char_manager_class, character1, character2
):
    mock_char_manager = Mock(spec=CharactersManager)
    mock_char_manager.get_characters_at_current_place_plus_followers.return_value = [
        character1,
        character2,
    ]
    mock_char_manager_class.return_value = mock_char_manager

    playthrough_name = "Adventure1"
    character_identifiers = ["char_2"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name, character_identifiers=character_identifiers
    )

    available_characters = algo.do_algorithm()

    # Should exclude character2
    assert available_characters == [character1]
    mock_char_manager_class.assert_called_once_with(playthrough_name)
    mock_char_manager.get_characters_at_current_place_plus_followers.assert_called_once()


# Test do_algorithm when all characters are excluded
def test_do_algorithm_all_characters_excluded(
    mock_characters_manager, character1, character2, character3
):
    playthrough_name = "Adventure1"
    character_identifiers = ["char_1", "char_2", "char_3"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    assert available_characters == []


# Test do_algorithm when no characters are excluded
def test_do_algorithm_no_characters_excluded(
    mock_characters_manager, character1, character2, character3
):
    playthrough_name = "Adventure1"
    character_identifiers = []  # No exclusions

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    assert available_characters == [character1, character2, character3]


# Test do_algorithm with empty list of all_characters
def test_do_algorithm_empty_all_characters(mock_characters_manager):
    mock_characters_manager.get_characters_at_current_place_plus_followers.return_value = (
        []
    )

    playthrough_name = "Adventure1"
    character_identifiers = ["char_1"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    assert available_characters == []


# Test do_algorithm with overlapping and non-overlapping identifiers
def test_do_algorithm_mixed_exclusions(
    mock_characters_manager, character1, character2, character3
):
    playthrough_name = "Adventure1"
    character_identifiers = ["char_2", "char_4"]  # char_4 doesn't exist

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    # Only char_2 is excluded
    assert available_characters == [character1, character3]


# Test initialization with CharactersManager returning duplicates
def test_do_algorithm_characters_manager_returns_duplicates(
    mock_characters_manager, character1
):
    mock_characters_manager.get_characters_at_current_place_plus_followers.return_value = [
        character1,
        character1,  # Duplicate
    ]

    playthrough_name = "Adventure1"
    character_identifiers = []

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    assert available_characters == [character1, character1]


# Test initialization with large number of characters
def test_do_algorithm_large_number_of_characters(mock_characters_manager):
    playthrough_name = "Adventure1"
    character_identifiers = [f"char_{i}" for i in range(1000)]

    # Create 1000 mock characters
    mock_characters = []
    for i in range(1000):
        char = Mock(spec=Character)
        char.identifier = f"char_{i}"
        mock_characters.append(char)

    mock_characters_manager.get_characters_at_current_place_plus_followers.return_value = (
        mock_characters
    )

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    available_characters = algo.do_algorithm()

    # All characters are excluded
    assert available_characters == []


# Test that do_algorithm handles characters with no identifier gracefully
def test_do_algorithm_character_without_identifier(mock_characters_manager):
    # Create a character without 'identifier' attribute
    char_without_id = Mock(spec=Character)
    del char_without_id.identifier  # Remove identifier

    mock_characters_manager.get_characters_at_current_place_plus_followers.return_value = [
        char_without_id
    ]

    playthrough_name = "Adventure1"
    character_identifiers = ["char_1"]

    algo = GetAvailableCharactersAlgorithm(
        playthrough_name=playthrough_name,
        character_identifiers=character_identifiers,
        characters_manager=mock_characters_manager,
    )

    with pytest.raises(AttributeError):
        algo.do_algorithm()
