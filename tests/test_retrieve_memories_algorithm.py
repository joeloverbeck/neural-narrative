# test_retrieve_memories_algorithm.py

from unittest.mock import Mock, patch

import pytest

from src.characters.algorithms.retrieve_memories_algorithm import (
    RetrieveMemoriesAlgorithm,
)
# Assuming the module path is as given in the user's code
from src.databases.abstracts.database import Database
from src.filesystem.config_loader import ConfigLoader


# Fixtures for commonly used mocks
@pytest.fixture
def mock_database():
    return Mock(spec=Database)


@pytest.fixture
def mock_config_loader():
    return Mock(spec=ConfigLoader)


@pytest.fixture
def valid_character_identifier():
    return "character_123"


@pytest.fixture
def valid_query_text():
    return "What are your memories about training?"


@pytest.fixture
def retrieve_memories_result():
    return ["Memory1", "Memory2", "Memory3"]


# Tests for Initialization
def test_init_with_valid_inputs(
    mock_database, valid_character_identifier, valid_query_text, mock_config_loader
):
    with patch(
        "src.characters.algorithms.retrieve_memories_algorithm.ConfigLoader"
    ) as MockConfigLoader:
        RetrieveMemoriesAlgorithm(
            character_identifier=valid_character_identifier,
            query_text=valid_query_text,
            database=mock_database,  # noqa
            config_loader=None,
        )

        # Check that validate_non_empty_string was called for both parameters
        with patch(
            "src.characters.algorithms.retrieve_memories_algorithm.validate_non_empty_string"
        ) as mock_validator:
            instance = RetrieveMemoriesAlgorithm(
                character_identifier=valid_character_identifier,
                query_text=valid_query_text,
                database=mock_database,  # noqa
                config_loader=None,
            )
            mock_validator.assert_any_call(
                valid_character_identifier, "character_identifier"
            )
            mock_validator.assert_any_call(valid_query_text, "query_text")

        # Check that attributes are set correctly
        assert instance._character_identifier == valid_character_identifier
        assert instance._query_text == valid_query_text
        assert instance._database == mock_database

        # Check that ConfigLoader was instantiated
        MockConfigLoader.assert_called()
        assert instance._config_loader == MockConfigLoader.return_value


def test_init_with_custom_config_loader(
    mock_database, valid_character_identifier, valid_query_text, mock_config_loader
):
    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    assert instance._config_loader == mock_config_loader


def test_init_with_empty_character_identifier(
    mock_database, valid_query_text, mock_config_loader
):
    with patch(
        "src.characters.algorithms.retrieve_memories_algorithm.validate_non_empty_string"
    ) as mock_validator:
        mock_validator.side_effect = lambda x, y: (_ for _ in ()).throw(
            ValueError("Empty string")
        )

        with pytest.raises(ValueError, match="Empty string"):
            RetrieveMemoriesAlgorithm(
                character_identifier="",
                query_text=valid_query_text,
                database=mock_database,  # noqa
                config_loader=None,
            )
        mock_validator.assert_called_with("", "character_identifier")


def test_init_with_empty_query_text(
    mock_database, valid_character_identifier, mock_config_loader
):
    with patch(
        "src.characters.algorithms.retrieve_memories_algorithm.validate_non_empty_string"
    ) as mock_validator:

        def side_effect(_x, y):
            if y == "query_text":
                raise ValueError("Empty string")

        mock_validator.side_effect = side_effect

        with pytest.raises(ValueError, match="Empty string"):
            RetrieveMemoriesAlgorithm(
                character_identifier=valid_character_identifier,
                query_text="",
                database=mock_database,  # noqa
                config_loader=None,
            )
        mock_validator.assert_any_call(
            valid_character_identifier, "character_identifier"
        )
        mock_validator.assert_any_call("", "query_text")


# Tests for do_algorithm Method
def test_do_algorithm_with_default_config_loader(
    mock_database,
    valid_character_identifier,
    valid_query_text,
    retrieve_memories_result,
):
    with patch(
        "src.characters.algorithms.retrieve_memories_algorithm.ConfigLoader"
    ) as MockConfigLoader:
        mock_config_loader_instance = MockConfigLoader.return_value
        mock_config_loader_instance.get_memories_to_retrieve_from_database.return_value = (
            5
        )

        instance = RetrieveMemoriesAlgorithm(
            character_identifier=valid_character_identifier,
            query_text=valid_query_text,
            database=mock_database,  # noqa
            config_loader=None,
        )

        mock_database.retrieve_memories.return_value = retrieve_memories_result

        result = instance.do_algorithm()

        # Verify that get_memories_to_retrieve_from_database was called
        mock_config_loader_instance.get_memories_to_retrieve_from_database.assert_called_once()

        # Verify that retrieve_memories was called with correct parameters
        mock_database.retrieve_memories.assert_called_once_with(
            valid_character_identifier, valid_query_text, 5
        )

        # Verify the result is as expected
        assert result == retrieve_memories_result


def test_do_algorithm_with_custom_config_loader(
    mock_database,
    valid_character_identifier,
    valid_query_text,
    mock_config_loader,
    retrieve_memories_result,
):
    mock_config_loader.get_memories_to_retrieve_from_database.return_value = 10

    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    mock_database.retrieve_memories.return_value = retrieve_memories_result

    result = instance.do_algorithm()

    # Verify that get_memories_to_retrieve_from_database was called on custom config_loader
    mock_config_loader.get_memories_to_retrieve_from_database.assert_called_once()

    # Verify that retrieve_memories was called with correct parameters
    mock_database.retrieve_memories.assert_called_once_with(
        valid_character_identifier, valid_query_text, 10
    )

    # Verify the result is as expected
    assert result == retrieve_memories_result


def test_do_algorithm_returns_correct_result(
    mock_database,
    valid_character_identifier,
    valid_query_text,
    mock_config_loader,
    retrieve_memories_result,
):
    mock_config_loader.get_memories_to_retrieve_from_database.return_value = 3
    mock_database.retrieve_memories.return_value = retrieve_memories_result

    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    result = instance.do_algorithm()

    assert result == retrieve_memories_result


# Additional Edge Case Tests
def test_do_algorithm_with_zero_memories(
    mock_database, valid_character_identifier, valid_query_text, mock_config_loader
):
    mock_config_loader.get_memories_to_retrieve_from_database.return_value = 0
    mock_database.retrieve_memories.return_value = []

    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    result = instance.do_algorithm()

    mock_database.retrieve_memories.assert_called_once_with(
        valid_character_identifier, valid_query_text, 0
    )
    assert result == []


def test_do_algorithm_with_exception_in_database(
    mock_database, valid_character_identifier, valid_query_text, mock_config_loader
):
    mock_config_loader.get_memories_to_retrieve_from_database.return_value = 5
    mock_database.retrieve_memories.side_effect = Exception("Database error")

    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    with pytest.raises(Exception, match="Database error"):
        instance.do_algorithm()


def test_do_algorithm_with_exception_in_config_loader(
    mock_database, valid_character_identifier, valid_query_text, mock_config_loader
):
    mock_config_loader.get_memories_to_retrieve_from_database.side_effect = Exception(
        "Config error"
    )

    instance = RetrieveMemoriesAlgorithm(
        character_identifier=valid_character_identifier,
        query_text=valid_query_text,
        database=mock_database,  # noqa
        config_loader=mock_config_loader,
    )

    with pytest.raises(Exception, match="Config error"):
        instance.do_algorithm()
