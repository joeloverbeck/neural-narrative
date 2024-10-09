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
            PartyDataForPromptFactory(playthrough_name="")

    def test_init_with_provided_managers(self):
        """Test that provided managers are used."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        assert factory._playthrough_manager is playthrough_manager
        assert factory._characters_manager is characters_manager

    def test_get_followers_data(self):
        """Test that _get_followers_data returns correct follower data."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        follower_ids = ["follower1", "follower2"]
        followers_data = [
            {"id": "follower1", "name": "Follower One"},
            {"id": "follower2", "name": "Follower Two"},
        ]
        playthrough_manager.get_followers.return_value = follower_ids
        characters_manager.get_full_data_of_characters.return_value = followers_data

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )

        result = factory._get_followers_data()
        assert result == followers_data
        playthrough_manager.get_followers.assert_called_once()
        characters_manager.get_full_data_of_characters.assert_called_once_with(
            follower_ids
        )

    def test_get_followers_data_empty_followers(self):
        """Test _get_followers_data when there are no followers."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        playthrough_manager.get_followers.return_value = []
        characters_manager.get_full_data_of_characters.return_value = []

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )

        result = factory._get_followers_data()
        assert result == []
        playthrough_manager.get_followers.assert_called_once()
        characters_manager.get_full_data_of_characters.assert_called_once_with([])

    def test_get_followers_information(self):
        """Test that _get_followers_information returns correctly formatted string."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        followers_data = [
            {
                "name": "Follower One",
                "description": "Description One",
                "personality": "Personality One",
                "profile": "Profile One",
                "likes": "Likes One",
                "dislikes": "Dislikes One",
                "speech patterns": "Speech Patterns One",
                "equipment": "Equipment One",
            },
            {
                "name": "Follower Two",
                "description": "Description Two",
                "personality": "Personality Two",
                "profile": "Profile Two",
                "likes": "Likes Two",
                "dislikes": "Dislikes Two",
                "speech patterns": "Speech Patterns Two",
                "equipment": "Equipment Two",
            },
        ]
        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=followers_data)

        expected_info = (
            f"- Follower name: Follower One\n"
            f"- Description: Description One\n"
            f"- Personality: Personality One\n"
            f"- Profile: Profile One\n"
            f"- Likes: Likes One\n"
            f"- Dislikes: Dislikes One\n"
            f"- Speech patterns: Speech Patterns One\n"
            f"- Equipment: Equipment One\n"
            "-----\n"
            f"- Follower name: Follower Two\n"
            f"- Description: Description Two\n"
            f"- Personality: Personality Two\n"
            f"- Profile: Profile Two\n"
            f"- Likes: Likes Two\n"
            f"- Dislikes: Dislikes Two\n"
            f"- Speech patterns: Speech Patterns Two\n"
            f"- Equipment: Equipment Two\n"
            "-----\n"
        )

        result = factory._get_followers_information()
        assert result == expected_info

    def test_get_followers_information_empty_followers(self):
        """Test _get_followers_information when there are no followers."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=[])

        result = factory._get_followers_information()
        assert result == ""

    def test_get_followers_information_missing_fields(self):
        """Test _get_followers_information with missing fields in follower data."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()
        followers_data = [
            {
                "name": "Follower One",
                "description": "Description One",
                # Missing 'personality' field
                "profile": "Profile One",
                "likes": "Likes One",
                "dislikes": "Dislikes One",
                "speech patterns": "Speech Patterns One",
                "equipment": "Equipment One",
            },
        ]
        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=followers_data)

        # The code is expected to raise a KeyError due to missing 'personality'
        with pytest.raises(KeyError):
            factory._get_followers_information()

    def test_get_followers_memories(self):
        """Test that _get_followers_memories returns combined followers' memories."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        followers_data = [
            {"identifier": "follower1"},
            {"identifier": "follower2"},
        ]
        memories_strs = {
            "follower1": "memory2\nmemory3",
            "follower2": "memory4\nmemory5",
        }

        characters_manager.load_character_memories.side_effect = (
            lambda identifier: memories_strs[identifier]
        )

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=followers_data)

        expected_followers_memories = ["memory2", "memory3", "memory4", "memory5"]

        result = factory._get_followers_memories()

        assert result == expected_followers_memories

    def test_get_followers_memories_empty_followers(self):
        """Test _get_followers_memories when there are no followers."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=[])

        result = factory._get_followers_memories()
        assert result == []

    def test_get_followers_memories_no_memories(self):
        """Test _get_followers_memories when followers have no memories."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        followers_data = [
            {"identifier": "follower1"},
        ]

        characters_manager.load_character_memories.return_value = ""

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=followers_data)

        result = factory._get_followers_memories()
        assert result == []

    def test_get_followers_memories_with_whitespace(self):
        """Test _get_followers_memories handles extra whitespace and empty lines."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        followers_data = [
            {"identifier": "follower1"},
        ]

        memories_str = "\n memory1 \n\n memory2 \n"
        expected_memories = ["memory1", "memory2"]

        characters_manager.load_character_memories.return_value = memories_str

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )
        factory._get_followers_data = MagicMock(return_value=followers_data)

        result = factory._get_followers_memories()
        assert result == expected_memories

    def test_get_party_data_for_prompt(self):
        """Test that get_party_data_for_prompt returns correct aggregated data."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        player_identifier = "player1"
        player_data = {
            "name": "Player One",
            "description": "Player Description",
            "personality": "Player Personality",
            "profile": "Player Profile",
            "likes": "Player Likes",
            "dislikes": "Player Dislikes",
            "speech patterns": "Player Speech Patterns",
            "equipment": "Player Equipment",
        }
        player_memories_str = "memory1\nmemory2"

        followers_information = "Followers info"

        followers_memories = ["memory2", "memory3", "memory4"]
        combined_memories = ["memory1", "memory2", "memory3", "memory4"]

        playthrough_manager.get_player_identifier.return_value = player_identifier
        characters_manager.load_character_data.return_value = player_data
        characters_manager.load_character_memories.return_value = player_memories_str

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )

        factory._get_followers_information = MagicMock(
            return_value=followers_information
        )
        factory._get_followers_memories = MagicMock(return_value=followers_memories)
        factory._get_combined_memories = MagicMock(return_value=combined_memories)

        result = factory.get_party_data_for_prompt()

        expected_result = {
            "player_name": player_data["name"],
            "player_description": player_data["description"],
            "player_personality": player_data["personality"],
            "player_profile": player_data["profile"],
            "player_likes": player_data["likes"],
            "player_dislikes": player_data["dislikes"],
            "player_speech_patterns": player_data["speech patterns"],
            "player_equipment": player_data["equipment"],
            "followers_information": followers_information,
            "combined_memories": combined_memories,
        }

        assert result == expected_result

    def test_get_party_data_for_prompt_no_memories(self):
        """Test get_party_data_for_prompt when player has no memories."""
        playthrough_name = "TestPlaythrough"
        playthrough_manager = MagicMock()
        characters_manager = MagicMock()

        player_identifier = "player1"
        player_data = {
            "name": "Player One",
            "description": "Player Description",
            "personality": "Player Personality",
            "profile": "Player Profile",
            "likes": "Player Likes",
            "dislikes": "Player Dislikes",
            "speech patterns": "Player Speech Patterns",
            "equipment": "Player Equipment",
        }
        player_memories_str = ""

        followers_information = ""
        followers_memories = []
        combined_memories = []

        playthrough_manager.get_player_identifier.return_value = player_identifier
        characters_manager.load_character_data.return_value = player_data
        characters_manager.load_character_memories.return_value = player_memories_str

        factory = PartyDataForPromptFactory(
            playthrough_name=playthrough_name,
            playthrough_manager=playthrough_manager,
            characters_manager=characters_manager,
        )

        factory._get_followers_information = MagicMock(
            return_value=followers_information
        )
        factory._get_followers_memories = MagicMock(return_value=followers_memories)
        factory._get_combined_memories = MagicMock(return_value=combined_memories)

        result = factory.get_party_data_for_prompt()

        expected_result = {
            "player_name": player_data["name"],
            "player_description": player_data["description"],
            "player_personality": player_data["personality"],
            "player_profile": player_data["profile"],
            "player_likes": player_data["likes"],
            "player_dislikes": player_data["dislikes"],
            "player_speech_patterns": player_data["speech patterns"],
            "player_equipment": player_data["equipment"],
            "followers_information": followers_information,
            "combined_memories": combined_memories,
        }

        assert result == expected_result
