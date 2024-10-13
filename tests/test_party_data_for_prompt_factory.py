from unittest.mock import MagicMock

import pytest

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)


# Assuming PartyDataForPromptFactory is imported from its module
# from src.party_data_for_prompt_factory import PartyDataForPromptFactory


class TestPartyDataForPromptFactory:
    def test_init_with_empty_playthrough_name(self):
        """Test that ValueError is raised when playthrough_name is empty."""
        with pytest.raises(ValueError, match="playthrough_name can't be empty."):
            PartyDataForPromptFactory(
                playthrough_name="", player_data_for_prompt_factory=MagicMock()
            )

    def test_init_with_provided_managers(self):
        """Test that provided managers are used."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            player_data_for_prompt_factory=MagicMock(),
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        assert factory._playthrough_manager is playthrough_manager
        assert factory._characters_manager is characters_manager

    def test_get_followers_information_empty_followers(self):
        """Test _get_followers_information when there are no followers."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            player_data_for_prompt_factory=MagicMock(),
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=[])

        result = factory._get_followers_information()
        assert result == ""

    def test_get_followers_memories_empty_followers(self):
        """Test _get_followers_memories when there are no followers."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            player_data_for_prompt_factory=MagicMock(),
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=[])

        result = factory._get_followers_memories()
        assert result == []
