from unittest.mock import MagicMock, patch

import pytest

from src.characters.providers.character_information_provider import (
    CharacterInformationProvider,
)


def test_get_information_returns_correct_string():
    # Mock dependencies
    character_identifier = "test_character"
    query_text = "test query"

    # Mock CharacterFactory
    mock_character = MagicMock()
    mock_character.name = "Test Name"
    mock_character.description = "Test Description"
    mock_character.personality = "Test Personality"
    mock_character.profile = "Test Profile"
    mock_character.likes = "Test Likes"
    mock_character.dislikes = "Test Dislikes"
    mock_character.secrets = "Test Secrets"
    mock_character.speech_patterns = "Test Speech Patterns"
    mock_character.health = "Test Health"
    mock_character.equipment = "Test Equipment"
    mock_character.identifier = "test_character"

    mock_character_factory = MagicMock()
    mock_character_factory.create_character.return_value = mock_character

    # Mock RetrieveMemoriesAlgorithmFactory
    mock_algorithm = MagicMock()
    mock_algorithm.do_algorithm.return_value = ["Memory 1", "Memory 2", "Memory 3"]

    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_retrieve_memories_algorithm_factory.create_algorithm.return_value = (
        mock_algorithm
    )

    # Mock PathManager
    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    # Mock read_file function
    character_information_template = (
        "Name: {name}\n"
        "Description: {description}\n"
        "Personality: {personality}\n"
        "Profile: {profile}\n"
        "Likes: {likes}\n"
        "Dislikes: {dislikes}\n"
        "Secrets: {secrets}\n"
        "Speech Patterns: {speech_patterns}\n"
        "Health: {health}\n"
        "Equipment: {equipment}\n"
        "Memories:\n{memories}"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        return_value=character_information_template,
    ) as mock_read_file:
        # Instantiate CharacterInformationProvider
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )

        # Call get_information
        result = provider.get_information()

        # Check that the result is as expected
        expected_result = (
            "Name: Test Name\n"
            "Description: Test Description\n"
            "Personality: Test Personality\n"
            "Profile: Test Profile\n"
            "Likes: Test Likes\n"
            "Dislikes: Test Dislikes\n"
            "Secrets: Test Secrets\n"
            "Speech Patterns: Test Speech Patterns\n"
            "Health: Test Health\n"
            "Equipment: Test Equipment\n"
            "Memories:\nMemory 1\nMemory 2\nMemory 3"
        )

        assert result == expected_result

        # Verify that create_character was called with the correct identifier
        mock_character_factory.create_character.assert_called_once_with(
            character_identifier
        )

        # Verify that retrieve_memories_algorithm_factory.create_algorithm was called with correct parameters
        mock_retrieve_memories_algorithm_factory.create_algorithm.assert_called_once_with(
            mock_character.identifier, query_text
        )

        # Verify that get_character_information_path was called
        mock_path_manager.get_character_information_path.assert_called_once()

        # Verify that read_file was called with the correct path
        mock_read_file.assert_called_once_with("fake/path/to/character_information.txt")


def test_init_with_empty_character_identifier_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        CharacterInformationProvider(
            character_identifier="",
            query_text="test query",
            retrieve_memories_algorithm_factory=MagicMock(),
            character_factory=MagicMock(),
            path_manager=MagicMock(),
        )
    assert "character_identifier" in str(exc_info.value)


def test_init_with_empty_query_text_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        CharacterInformationProvider(
            character_identifier="test_character",
            query_text="",
            retrieve_memories_algorithm_factory=MagicMock(),
            character_factory=MagicMock(),
            path_manager=MagicMock(),
        )
    assert "query_text" in str(exc_info.value)


def test_init_with_none_path_manager_uses_default():
    with patch(
        "src.characters.providers.character_information_provider.PathManager"
    ) as MockPathManager:
        provider = CharacterInformationProvider(
            character_identifier="test_character",
            query_text="test query",
            retrieve_memories_algorithm_factory=MagicMock(),
            character_factory=MagicMock(),
            path_manager=None,
        )
        # Check that PathManager was instantiated
        MockPathManager.assert_called_once()
        # Ensure that self._path_manager is set to the instance of PathManager
        assert provider._path_manager == MockPathManager.return_value


def test_get_information_with_missing_placeholders():
    # Mock dependencies
    character_identifier = "test_character"
    query_text = "test query"

    mock_character = MagicMock()
    mock_character.name = "Test Name"
    mock_character.description = "Test Description"
    mock_character.identifier = character_identifier

    mock_character_factory = MagicMock()
    mock_character_factory.create_character.return_value = mock_character

    mock_algorithm = MagicMock()
    mock_algorithm.do_algorithm.return_value = ["Memory 1", "Memory 2", "Memory 3"]

    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_retrieve_memories_algorithm_factory.create_algorithm.return_value = (
        mock_algorithm
    )

    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    # Template with missing placeholders
    character_information_template = (
        "Name: {name}\n" "Description: {description}\n" "Memories:\n{memories}"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        return_value=character_information_template,
    ):
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )
        result = provider.get_information()

        expected_result = (
            "Name: Test Name\n"
            "Description: Test Description\n"
            "Memories:\nMemory 1\nMemory 2\nMemory 3"
        )
        assert result == expected_result


def test_get_information_handles_read_file_exception():
    character_identifier = "test_character"
    query_text = "test query"

    mock_character_factory = MagicMock()
    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        side_effect=FileNotFoundError,
    ):
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )

        with pytest.raises(FileNotFoundError):
            provider.get_information()


def test_get_information_handles_character_factory_exception():
    character_identifier = "test_character"
    query_text = "test query"

    mock_character_factory = MagicMock()
    mock_character_factory.create_character.side_effect = Exception(
        "Character creation failed"
    )
    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        return_value="",
    ):
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )

        with pytest.raises(Exception) as exc_info:
            provider.get_information()
        assert "Character creation failed" in str(exc_info.value)


def test_get_information_handles_memory_retrieval_exception():
    character_identifier = "test_character"
    query_text = "test query"

    mock_character = MagicMock()
    mock_character.identifier = character_identifier

    mock_character_factory = MagicMock()
    mock_character_factory.create_character.return_value = mock_character

    mock_algorithm = MagicMock()
    mock_algorithm.do_algorithm.side_effect = Exception("Memory retrieval failed")

    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_retrieve_memories_algorithm_factory.create_algorithm.return_value = (
        mock_algorithm
    )

    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        return_value="",
    ):
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )

        with pytest.raises(Exception) as exc_info:
            provider.get_information()
        assert "Memory retrieval failed" in str(exc_info.value)


def test_get_information_handles_template_formatting_exception():
    character_identifier = "test_character"
    query_text = "test query"

    mock_character = MagicMock()
    mock_character.name = "Test Name"
    mock_character.identifier = character_identifier

    mock_character_factory = MagicMock()
    mock_character_factory.create_character.return_value = mock_character

    mock_algorithm = MagicMock()
    mock_algorithm.do_algorithm.return_value = ["Memory 1", "Memory 2", "Memory 3"]

    mock_retrieve_memories_algorithm_factory = MagicMock()
    mock_retrieve_memories_algorithm_factory.create_algorithm.return_value = (
        mock_algorithm
    )

    mock_path_manager = MagicMock()
    mock_path_manager.get_character_information_path.return_value = (
        "fake/path/to/character_information.txt"
    )

    # Template with invalid placeholder
    character_information_template = (
        "Name: {name}\n"
        "Invalid Placeholder: {invalid_placeholder}\n"
        "Memories:\n{memories}"
    )

    with patch(
        "src.characters.providers.character_information_provider.read_file",
        return_value=character_information_template,
    ):
        provider = CharacterInformationProvider(
            character_identifier=character_identifier,
            query_text=query_text,
            retrieve_memories_algorithm_factory=mock_retrieve_memories_algorithm_factory,
            character_factory=mock_character_factory,
            path_manager=mock_path_manager,
        )
        with pytest.raises(KeyError) as exc_info:
            provider.get_information()
        assert "invalid_placeholder" in str(exc_info.value)
