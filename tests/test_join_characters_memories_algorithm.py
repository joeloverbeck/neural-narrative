# test_join_characters_memories_algorithm.py

from unittest.mock import Mock, call

import pytest

# Adjust the import path based on your project structure
from src.characters.algorithms.join_characters_memories_algorithm import (
    JoinCharactersMemoriesAlgorithm,
)
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)


# Assuming validate_non_empty_string raises ValueError for invalid inputs
def test_init_with_valid_inputs():
    character_identifiers = ["char1", "char2"]
    query_text = "Retrieve memories"
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    assert algo._character_identifiers == character_identifiers
    assert algo._query_text == query_text
    assert algo._retrieve_memories_algorithm_factories == mock_factory


def test_init_with_empty_query_text():
    character_identifiers = ["char1", "char2"]
    query_text = ""
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    with pytest.raises(ValueError) as exc_info:
        JoinCharactersMemoriesAlgorithm(
            character_identifiers=character_identifiers,
            query_text=query_text,
            retrieve_memories_algorithm_factories=mock_factory,
        )
    assert "query_text" in str(exc_info.value)


def test_init_with_non_string_query_text():
    character_identifiers = ["char1", "char2"]
    query_text = None  # Non-string input
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    with pytest.raises(ValueError) as exc_info:
        JoinCharactersMemoriesAlgorithm(
            character_identifiers=character_identifiers,
            query_text=query_text,  # noqa
            retrieve_memories_algorithm_factories=mock_factory,
        )
    assert "query_text" in str(exc_info.value)


def test_do_algorithm_with_empty_character_identifiers():
    character_identifiers = []
    query_text = "Retrieve memories"
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    result = algo.do_algorithm()
    assert result == []
    mock_factory.create_algorithm.assert_not_called()


def test_do_algorithm_with_single_character_identifier():
    character_identifiers = ["char1"]
    query_text = "Retrieve memories"

    # Mock the factory and algorithm
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)
    mock_algorithm = Mock()
    mock_algorithm.do_algorithm.return_value = ["memory1", "memory2"]
    mock_factory.create_algorithm.return_value = mock_algorithm

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    result = algo.do_algorithm()
    assert result == ["memory1", "memory2"]
    mock_factory.create_algorithm.assert_called_once_with("char1", query_text)
    mock_algorithm.do_algorithm.assert_called_once()


def test_do_algorithm_with_multiple_character_identifiers():
    character_identifiers = ["char1", "char2", "char3"]
    query_text = "Retrieve memories"

    # Mock the factory and algorithms
    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    mock_algorithm1 = Mock()
    mock_algorithm1.do_algorithm.return_value = ["memory1", "memory2"]

    mock_algorithm2 = Mock()
    mock_algorithm2.do_algorithm.return_value = ["memory3"]

    mock_algorithm3 = Mock()
    mock_algorithm3.do_algorithm.return_value = ["memory4", "memory5", "memory6"]

    # Setup the factory to return different algorithms based on input
    mock_factory.create_algorithm.side_effect = [
        mock_algorithm1,
        mock_algorithm2,
        mock_algorithm3,
    ]

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    result = algo.do_algorithm()
    expected = ["memory1", "memory2", "memory3", "memory4", "memory5", "memory6"]
    assert result == expected

    # Check that create_algorithm was called correctly
    expected_calls = [
        call("char1", query_text),
        call("char2", query_text),
        call("char3", query_text),
    ]
    assert mock_factory.create_algorithm.call_args_list == expected_calls

    # Check that do_algorithm was called on each algorithm
    mock_algorithm1.do_algorithm.assert_called_once()
    mock_algorithm2.do_algorithm.assert_called_once()
    mock_algorithm3.do_algorithm.assert_called_once()


def test_do_algorithm_propagates_factory_exception():
    character_identifiers = ["char1", "char2"]
    query_text = "Retrieve memories"

    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)
    mock_factory.create_algorithm.side_effect = Exception("Factory error")

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    with pytest.raises(Exception) as exc_info:
        algo.do_algorithm()
    assert "Factory error" in str(exc_info.value)
    mock_factory.create_algorithm.assert_called_once_with("char1", query_text)


def test_do_algorithm_propagates_algorithm_exception():
    character_identifiers = ["char1", "char2"]
    query_text = "Retrieve memories"

    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    mock_algorithm1 = Mock()
    mock_algorithm1.do_algorithm.return_value = ["memory1"]

    mock_algorithm2 = Mock()
    mock_algorithm2.do_algorithm.side_effect = Exception("Algorithm error")

    mock_factory.create_algorithm.side_effect = [
        mock_algorithm1,
        mock_algorithm2,
    ]

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    with pytest.raises(Exception) as exc_info:
        algo.do_algorithm()
    assert "Algorithm error" in str(exc_info.value)

    # Ensure both algorithms were attempted
    assert mock_factory.create_algorithm.call_args_list == [
        call("char1", query_text),
        call("char2", query_text),
    ]
    mock_algorithm1.do_algorithm.assert_called_once()
    mock_algorithm2.do_algorithm.assert_called_once()


def test_do_algorithm_with_duplicate_character_identifiers():
    character_identifiers = ["char1", "char1"]
    query_text = "Retrieve memories"

    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    mock_algorithm = Mock()
    mock_algorithm.do_algorithm.return_value = ["memory1"]

    mock_factory.create_algorithm.return_value = mock_algorithm

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    result = algo.do_algorithm()
    assert result == ["memory1"]
    assert mock_factory.create_algorithm.call_count == 1
    mock_factory.create_algorithm.assert_called_with("char1", query_text)
    mock_algorithm.do_algorithm.assert_called_once()


def test_do_algorithm_with_large_number_of_characters():
    character_identifiers = [f"char{i}" for i in range(100)]
    query_text = "Retrieve memories"

    mock_factory = Mock(spec=RetrieveMemoriesAlgorithmFactory)

    # Each algorithm returns a single memory
    mock_algorithm = Mock()
    mock_algorithm.do_algorithm.side_effect = lambda: [
        f"memory{mock_factory.create_algorithm.call_count}"
    ]
    mock_factory.create_algorithm.return_value = mock_algorithm

    algo = JoinCharactersMemoriesAlgorithm(
        character_identifiers=character_identifiers,
        query_text=query_text,
        retrieve_memories_algorithm_factories=mock_factory,
    )

    result = algo.do_algorithm()
    assert len(result) == 100
    assert result == [f"memory{i+1}" for i in range(100)]
    assert mock_factory.create_algorithm.call_count == 100
