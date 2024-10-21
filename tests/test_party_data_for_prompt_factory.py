# Assuming PartyDataForPromptFactory is imported from its module
# from src.party_data_for_prompt_factory import PartyDataForPromptFactory


class TestPartyDataForPromptFactory:
    def test_init_with_provided_managers(self):
        """Test that provided managers are used."""
        playthrough_name = RequiredString("TestPlaythrough")
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
        playthrough_name = RequiredString("TestPlaythrough")
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
        assert result is None

    def test_get_followers_memories_empty_followers(self):
        """Test _get_followers_memories when there are no followers."""
        playthrough_name = RequiredString("TestPlaythrough")
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


from unittest.mock import MagicMock

from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.characters.characters_manager import CharactersManager
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


def test_party_data_for_prompt_factory_init():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)
    character_memories = MagicMock(spec=CharacterMemories)

    factory = PartyDataForPromptFactory(
        playthrough_name,
        player_data_for_prompt_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
        character_memories=character_memories,
    )

    assert factory._player_data_for_prompt_factory == player_data_for_prompt_factory
    assert factory._playthrough_manager == playthrough_manager
    assert factory._characters_manager == characters_manager
    assert factory._character_memories == character_memories


def test_get_followers_data():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    playthrough_manager = MagicMock(spec=PlaythroughManager)
    characters_manager = MagicMock(spec=CharactersManager)

    follower_ids = ["follower1", "follower2"]
    playthrough_manager.get_followers.return_value = follower_ids

    followers_data = [MagicMock(spec=Character), MagicMock(spec=Character)]
    characters_manager.get_characters.return_value = followers_data

    factory = PartyDataForPromptFactory(
        playthrough_name,
        player_data_for_prompt_factory,
        playthrough_manager=playthrough_manager,
        characters_manager=characters_manager,
    )

    result = factory._get_followers_data()

    playthrough_manager.get_followers.assert_called_once()
    characters_manager.get_characters.assert_called_once_with(follower_ids)

    assert result == followers_data


def test_get_followers_information_with_followers():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    factory = PartyDataForPromptFactory(
        playthrough_name, player_data_for_prompt_factory
    )

    followers_data = [MagicMock(spec=Character), MagicMock(spec=Character)]
    followers_data[0].name = RequiredString("Follower1")
    followers_data[0].description = RequiredString("Desc1")
    followers_data[0].personality = RequiredString("Personality1")
    followers_data[0].profile = RequiredString("Profile1")
    followers_data[0].likes = "Likes1"
    followers_data[0].dislikes = "Dislikes1"
    followers_data[0].speech_patterns = "SpeechPatterns1"
    followers_data[0].equipment = RequiredString("Equipment1")

    followers_data[1].name = RequiredString("Follower2")
    followers_data[1].description = RequiredString("Desc2")
    followers_data[1].personality = RequiredString("Personality2")
    followers_data[1].profile = RequiredString("Profile2")
    followers_data[1].likes = "Likes2"
    followers_data[1].dislikes = "Dislikes2"
    followers_data[1].speech_patterns = "SpeechPatterns2"
    followers_data[1].equipment = RequiredString("Equipment2")

    factory._get_followers_data = MagicMock(return_value=followers_data)

    result = factory._get_followers_information()

    expected_info = (
        f"- Follower name: {followers_data[0].name}\n"
        f"- Description: {followers_data[0].description}\n"
        f"- Personality: {followers_data[0].personality}\n"
        f"- Profile: {followers_data[0].profile}\n"
        f"- Likes: {followers_data[0].likes}\n"
        f"- Dislikes: {followers_data[0].dislikes}\n"
        f"- Speech patterns: {followers_data[0].speech_patterns}\n"
        f"- Equipment: {followers_data[0].equipment}\n-----\n"
        f"- Follower name: {followers_data[1].name}\n"
        f"- Description: {followers_data[1].description}\n"
        f"- Personality: {followers_data[1].personality}\n"
        f"- Profile: {followers_data[1].profile}\n"
        f"- Likes: {followers_data[1].likes}\n"
        f"- Dislikes: {followers_data[1].dislikes}\n"
        f"- Speech patterns: {followers_data[1].speech_patterns}\n"
        f"- Equipment: {followers_data[1].equipment}\n-----\n"
    )
    assert result == RequiredString(expected_info)


def test_get_followers_information_no_followers():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    factory = PartyDataForPromptFactory(
        playthrough_name, player_data_for_prompt_factory
    )

    factory._get_followers_data = MagicMock(return_value=[])

    result = factory._get_followers_information()

    assert result is None


def test_get_combined_memories():
    player_memories = [RequiredString("memory1"), RequiredString("memory2")]
    followers_memories = [RequiredString("memory2"), RequiredString("memory3")]

    combined = PartyDataForPromptFactory._get_combined_memories(
        player_memories, followers_memories
    )

    expected = [
        RequiredString("memory1"),
        RequiredString("memory2"),
        RequiredString("memory3"),
    ]
    assert combined == expected


def test_get_party_data_for_prompt():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    factory = PartyDataForPromptFactory(
        playthrough_name, player_data_for_prompt_factory
    )

    player_data_for_prompt = MagicMock()
    player_data_for_prompt.get_player_memories.return_value = [
        RequiredString("memory1")
    ]
    player_data_for_prompt.get_player_data_for_prompt.return_value = {"key1": "value1"}

    player_data_for_prompt_factory.create_player_data_for_prompt.return_value = (
        player_data_for_prompt
    )

    factory._get_followers_information = MagicMock(
        return_value=RequiredString("followers_info")
    )
    factory._get_followers_memories = MagicMock(
        return_value=[RequiredString("memory2")]
    )

    combined_memories = [RequiredString("memory1"), RequiredString("memory2")]

    factory._get_combined_memories = MagicMock(return_value=combined_memories)

    result = factory.get_party_data_for_prompt()

    expected_data_for_prompt = {
        "key1": "value1",
        "followers_information": RequiredString("followers_info"),
        "combined_memories": combined_memories,
    }

    assert result == expected_data_for_prompt

    player_data_for_prompt_factory.create_player_data_for_prompt.assert_called_once()
    player_data_for_prompt.get_player_memories.assert_called_once()
    factory._get_followers_information.assert_called_once()
    factory._get_followers_memories.assert_called_once()
    factory._get_combined_memories.assert_called_once_with(
        player_data_for_prompt.get_player_memories.return_value,
        factory._get_followers_memories.return_value,
    )


def test_get_followers_memories():
    playthrough_name = RequiredString("test_playthrough")
    player_data_for_prompt_factory = MagicMock(spec=PlayerDataForPromptFactory)
    character_memories = MagicMock(spec=CharacterMemories)
    factory = PartyDataForPromptFactory(
        playthrough_name,
        player_data_for_prompt_factory,
        character_memories=character_memories,
    )

    followers_data = [MagicMock(spec=Character), MagicMock(spec=Character)]

    followers_data[0].name = RequiredString("Follower1")
    followers_data[1].name = RequiredString("Follower2")

    factory._get_followers_data = MagicMock(return_value=followers_data)

    memory_str1 = RequiredString("Memory A\nMemory B")
    memory_str2 = RequiredString("Memory B\nMemory C")
    character_memories.load_memories.side_effect = [memory_str1, memory_str2]

    result = factory._get_followers_memories()

    expected_memories = [
        RequiredString("Memory A"),
        RequiredString("Memory B"),
        RequiredString("Memory B"),
        RequiredString("Memory C"),
    ]
    assert result == expected_memories

    character_memories.load_memories.assert_any_call(followers_data[0])
    character_memories.load_memories.assert_any_call(followers_data[1])


def test_get_combined_memories_removes_duplicates():
    player_memories = [
        RequiredString("memory1"),
        RequiredString("memory2"),
        RequiredString("memory3"),
    ]
    followers_memories = [
        RequiredString("memory2"),
        RequiredString("memory3"),
        RequiredString("memory4"),
    ]

    combined = PartyDataForPromptFactory._get_combined_memories(
        player_memories, followers_memories
    )

    expected = [
        RequiredString("memory1"),
        RequiredString("memory2"),
        RequiredString("memory3"),
        RequiredString("memory4"),
    ]
    assert combined == expected


def test_get_combined_memories_preserves_order():
    player_memories = [
        RequiredString("memory3"),
        RequiredString("memory2"),
        RequiredString("memory1"),
    ]
    followers_memories = [
        RequiredString("memory4"),
        RequiredString("memory2"),
        RequiredString("memory5"),
    ]

    combined = PartyDataForPromptFactory._get_combined_memories(
        player_memories, followers_memories
    )

    expected = [
        RequiredString("memory3"),
        RequiredString("memory2"),
        RequiredString("memory1"),
        RequiredString("memory4"),
        RequiredString("memory5"),
    ]
    assert combined == expected
