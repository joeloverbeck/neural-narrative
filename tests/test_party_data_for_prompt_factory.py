# tests/test_party_data_for_prompt_factory.py
from typing import cast
from unittest.mock import Mock, patch

import pytest

from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.characters_manager import CharactersManager
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.characters.factories.prettified_memories_factory import (
    PrettifiedMemoriesFactory,
)


@pytest.fixture
def mock_other_characters_identifiers_strategy():
    return Mock(spec=OtherCharactersIdentifiersStrategy)


@pytest.fixture
def mock_player_data_for_prompt_factory():
    mock_factory = Mock(spec=PlayerDataForPromptFactory)
    mock_player_data = Mock()
    mock_player_data.get_player_data_for_prompt.return_value = {
        "player_key": "player_value"
    }
    mock_factory.create_player_data_for_prompt.return_value = mock_player_data
    return mock_factory


@pytest.fixture
def mock_prettified_memories_factory():
    mock_factory = Mock(spec=PrettifiedMemoriesFactory)
    mock_factory.create_prettified_memories.return_value = "prettified_memories"
    return mock_factory


@pytest.fixture
def mock_characters_manager():
    mock_manager = Mock(spec=CharactersManager)
    mock_manager.get_characters.return_value = ["char1", "char2"]
    mock_manager.get_characters_info.return_value = {"char_info_key": "char_info_value"}
    return mock_manager


@pytest.fixture
def factory_instance(
    mock_other_characters_identifiers_strategy,
    mock_player_data_for_prompt_factory,
    mock_prettified_memories_factory,
    mock_characters_manager,
):
    return PartyDataForPromptFactory(
        playthrough_name="TestPlaythrough",
        other_characters_role="TestRole",
        other_characters_identifiers_strategy=cast(
            OtherCharactersIdentifiersStrategy,
            mock_other_characters_identifiers_strategy,
        ),
        player_data_for_prompt_factory=mock_player_data_for_prompt_factory,
        prettified_memories_factory=mock_prettified_memories_factory,
        characters_manager=mock_characters_manager,
    )


@patch(
    "src.characters.factories.party_data_for_prompt_factory.validate_non_empty_string"
)
def test_initialization_valid(
    mock_validate_non_empty_string,
    mock_other_characters_identifiers_strategy,
    mock_player_data_for_prompt_factory,
    mock_prettified_memories_factory,
    mock_characters_manager,
):
    factory = PartyDataForPromptFactory(
        playthrough_name="Playthrough1",
        other_characters_role="Role1",
        other_characters_identifiers_strategy=cast(
            OtherCharactersIdentifiersStrategy,
            mock_other_characters_identifiers_strategy,
        ),
        player_data_for_prompt_factory=mock_player_data_for_prompt_factory,
        prettified_memories_factory=mock_prettified_memories_factory,
        characters_manager=mock_characters_manager,
    )

    mock_validate_non_empty_string.assert_any_call("Playthrough1", "playthrough_name")
    mock_validate_non_empty_string.assert_any_call("Role1", "other_characters_role")
    assert factory._other_characters_role == "Role1"
    assert (
        factory._other_characters_identifiers_strategy
        == mock_other_characters_identifiers_strategy
    )
    assert (
        factory._player_data_for_prompt_factory == mock_player_data_for_prompt_factory
    )
    assert factory._prettified_memories_factory == mock_prettified_memories_factory
    assert factory._characters_manager == mock_characters_manager


@patch(
    "src.characters.factories.party_data_for_prompt_factory.validate_non_empty_string"
)
def test_initialization_with_default_characters_manager(
    _mock_validate_non_empty_string,
    mock_other_characters_identifiers_strategy,
    mock_player_data_for_prompt_factory,
    mock_prettified_memories_factory,
):
    with patch(
        "src.characters.factories.party_data_for_prompt_factory.CharactersManager"
    ) as MockCharactersManager:
        mock_char_manager_instance = MockCharactersManager.return_value
        factory = PartyDataForPromptFactory(
            playthrough_name="Playthrough2",
            other_characters_role="Role2",
            other_characters_identifiers_strategy=cast(
                OtherCharactersIdentifiersStrategy,
                mock_other_characters_identifiers_strategy,
            ),
            player_data_for_prompt_factory=mock_player_data_for_prompt_factory,
            prettified_memories_factory=mock_prettified_memories_factory,
        )

        MockCharactersManager.assert_called_once_with("Playthrough2")
        assert factory._characters_manager == mock_char_manager_instance


@pytest.mark.parametrize(
    "playthrough_name, other_characters_role, expected_exception",
    [
        ("", "Role", ValueError),
        ("Playthrough", "", ValueError),
        ("", "", ValueError),
    ],
)
@patch(
    "src.characters.factories.party_data_for_prompt_factory.validate_non_empty_string"
)
def test_initialization_validation_errors(
    mock_validate_non_empty_string,
    playthrough_name,
    other_characters_role,
    expected_exception,
):
    mock_validate_non_empty_string.side_effect = lambda x, y: x or (
        _ for _ in ()
    ).throw(ValueError(f"{y} cannot be empty"))

    with pytest.raises(expected_exception) as exc_info:
        PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            other_characters_role=other_characters_role,
            other_characters_identifiers_strategy=cast(
                OtherCharactersIdentifiersStrategy, Mock()
            ),
            player_data_for_prompt_factory=Mock(),
            prettified_memories_factory=Mock(),
        )

    assert str(exc_info.value) in [
        "playthrough_name cannot be empty",
        "other_characters_role cannot be empty",
    ]


def test_get_party_data_for_prompt(factory_instance):
    # Arrange: Set up return values before calling the method
    factory_instance._player_data_for_prompt_factory.create_player_data_for_prompt.return_value.get_player_data_for_prompt.return_value = {  # noqa
        "player_key": "player_value"
    }
    factory_instance._other_characters_identifiers_strategy.get_data.return_value = [
        "char1",
        "char2",
    ]
    factory_instance._characters_manager.get_characters.return_value = [
        "char1",
        "char2",
    ]
    factory_instance._characters_manager.get_characters_info.return_value = {
        "char_info_key": "char_info_value"
    }
    factory_instance._prettified_memories_factory.create_prettified_memories.return_value = (
        "prettified_memories"
    )

    # Act: Call the method after setting up mocks
    result = factory_instance.get_party_data_for_prompt()

    # Assert: Verify that all methods were called as expected
    # Verify player data
    factory_instance._player_data_for_prompt_factory.create_player_data_for_prompt.assert_called_once()  # noqa
    factory_instance._player_data_for_prompt_factory.create_player_data_for_prompt.return_value.get_player_data_for_prompt.assert_called_once()  # noqa

    # Verify other characters identifiers strategy
    factory_instance._other_characters_identifiers_strategy.get_data.assert_called_once()

    # Verify characters manager interactions
    factory_instance._characters_manager.get_characters.assert_called_once_with(
        ["char1", "char2"]
    )
    factory_instance._characters_manager.get_characters_info.assert_called_once_with(
        ["char1", "char2"], "TestRole"
    )

    # Verify prettified memories
    factory_instance._prettified_memories_factory.create_prettified_memories.assert_called_once()  # noqa

    # Verify the result
    expected_data = {
        "player_key": "player_value",
        "other_characters_information": {"char_info_key": "char_info_value"},
        "combined_memories": "prettified_memories",
    }

    assert result == expected_data


def test_get_party_data_for_prompt_with_empty_other_characters_info(
    factory_instance, mock_characters_manager
):
    # Configure get_characters_info to return None or empty
    mock_characters_manager.get_characters_info.return_value = None

    result = factory_instance.get_party_data_for_prompt()

    expected_data = {
        "player_key": "player_value",
        "other_characters_information": "",
        "combined_memories": "prettified_memories",
    }

    assert result == expected_data


def test_get_party_data_for_prompt_characters_manager_not_provided():
    with patch(
        "src.characters.factories.party_data_for_prompt_factory.CharactersManager"
    ) as MockCharactersManager:
        mock_char_manager_instance = MockCharactersManager.return_value
        mock_char_manager_instance.get_characters.return_value = ["char1", "char2"]
        mock_char_manager_instance.get_characters_info.return_value = {
            "char_info_key": "char_info_value"
        }

        factory = PartyDataForPromptFactory(
            playthrough_name="Playthrough3",
            other_characters_role="Role3",
            other_characters_identifiers_strategy=cast(
                OtherCharactersIdentifiersStrategy,
                Mock(spec=OtherCharactersIdentifiersStrategy),
            ),
            player_data_for_prompt_factory=Mock(spec=PlayerDataForPromptFactory),
            prettified_memories_factory=Mock(spec=PrettifiedMemoriesFactory),
        )

        factory._player_data_for_prompt_factory.create_player_data_for_prompt.return_value.get_player_data_for_prompt.return_value = {  # noqa
            "player_key": "player_value"
        }
        factory._other_characters_identifiers_strategy.get_data.return_value = [
            "char1",
            "char2",
        ]
        factory._prettified_memories_factory.create_prettified_memories.return_value = (
            "prettified_memories"
        )

        result = factory.get_party_data_for_prompt()

        MockCharactersManager.assert_called_once_with("Playthrough3")
        assert factory._characters_manager == mock_char_manager_instance

        expected_data = {
            "player_key": "player_value",
            "other_characters_information": {"char_info_key": "char_info_value"},
            "combined_memories": "prettified_memories",
        }

        assert result == expected_data
