# tests/test_participants_manager.py

from unittest.mock import MagicMock, patch

import pytest

from src.characters.characters_manager import CharactersManager
from src.characters.participants_manager import ParticipantsManager
from src.playthrough_manager import PlaythroughManager


@pytest.fixture
def playthrough_name():
    return "TestPlaythrough"


@pytest.fixture
def mock_character_manager():
    with patch(
        "src.characters.characters_manager.CharactersManager"
    ) as MockCharactersManager:
        yield MockCharactersManager


@pytest.fixture
def mock_playthrough_manager():
    with patch("src.playthrough_manager.PlaythroughManager") as MockPlaythroughManager:
        yield MockPlaythroughManager


@pytest.fixture
def participants_manager(
    playthrough_name, mock_character_manager, mock_playthrough_manager
):
    return ParticipantsManager(playthrough_name)


def test_initialization_with_provided_managers(
    playthrough_name, mock_character_manager, mock_playthrough_manager
):
    custom_char_manager = MagicMock(spec=CharactersManager)
    custom_play_manager = MagicMock(spec=PlaythroughManager)

    pm = ParticipantsManager(
        playthrough_name,
        character_manager=custom_char_manager,
        playthrough_manager=custom_play_manager,
    )

    mock_character_manager.assert_not_called()
    mock_playthrough_manager.assert_not_called()
    assert pm._character_manager == custom_char_manager
    assert pm._playthrough_manager == custom_play_manager
