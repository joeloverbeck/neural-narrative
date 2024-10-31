from unittest.mock import Mock

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_memories_manager import CharacterMemoriesManager
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


def test_player_data_for_prompt_factory_initialization_with_provided_arguments():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    assert factory._playthrough_manager is playthrough_manager
    assert factory._character_memories is character_memories


def test_player_data_for_prompt_factory_create_player_data_for_prompt():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    player_identifier = "Player1"
    playthrough_manager.get_player_identifier.return_value = player_identifier
    player = Mock()
    player.name = "TestPlayer"
    player.description = "A brave warrior"
    player.personality = "Bold and fearless"
    player.profile = "Profile info"
    player.likes = "Adventure"
    player.dislikes = "Cowardice"
    player.secrets = "Secret identity"
    player.speech_patterns = "Speaks with confidence"
    player.health = 100
    player.equipment = "Sword and shield"
    character_factory.create_character.return_value = player
    memories = "Memory1\nMemory2\n"
    character_memories.load_memories.return_value = memories
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    player_data_for_prompt = factory.create_player_data_for_prompt()
    playthrough_manager.get_player_identifier.assert_called_once()
    character_factory.create_character.assert_called_once_with(player_identifier)
    character_memories.load_memories.assert_called_once_with(player)
    expected_player_data = {
        "player_name": player.name,
        "player_description": player.description,
        "player_personality": player.personality,
        "player_profile": player.profile,
        "player_likes": player.likes,
        "player_dislikes": player.dislikes,
        "player_secrets": player.secrets,
        "player_speech_patterns": player.speech_patterns,
        "player_health": player.health,
        "player_equipment": player.equipment,
    }
    assert player_data_for_prompt.get_player_data_for_prompt() == expected_player_data
    assert player_data_for_prompt.get_player_memories() == ["Memory1", "Memory2"]


def test_player_data_for_prompt_factory_create_player_data_for_prompt_no_memories():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    player_identifier = "Player1"
    playthrough_manager.get_player_identifier.return_value = player_identifier
    player = Mock()
    player.name = "TestPlayer"
    player.description = "A brave warrior"
    player.personality = "Bold and fearless"
    player.profile = "Profile info"
    player.likes = "Adventure"
    player.dislikes = "Cowardice"
    player.secrets = "Secret identity"
    player.speech_patterns = "Speaks with confidence"
    player.health = 100
    player.equipment = "Sword and shield"
    character_factory.create_character.return_value = player
    character_memories.load_memories.return_value = None
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    player_data_for_prompt = factory.create_player_data_for_prompt()
    expected_player_data = {
        "player_name": player.name,
        "player_description": player.description,
        "player_personality": player.personality,
        "player_profile": player.profile,
        "player_likes": player.likes,
        "player_dislikes": player.dislikes,
        "player_secrets": player.secrets,
        "player_speech_patterns": player.speech_patterns,
        "player_health": player.health,
        "player_equipment": player.equipment,
    }
    assert player_data_for_prompt.get_player_data_for_prompt() == expected_player_data
    assert player_data_for_prompt.get_player_memories() == []


def test_player_data_for_prompt_factory_create_player_data_for_prompt_with_whitespace_memories():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    player_identifier = "Player1"
    playthrough_manager.get_player_identifier.return_value = player_identifier
    player = Mock()
    player.name = "TestPlayer"
    player.description = "A brave warrior"
    player.personality = "Bold and fearless"
    player.profile = "Profile info"
    player.likes = "Adventure"
    player.dislikes = "Cowardice"
    player.secrets = "Secret identity"
    player.speech_patterns = "Speaks with confidence"
    player.health = 100
    player.equipment = "Sword and shield"
    character_factory.create_character.return_value = player
    memories = "Memory1\n\n  \nMemory2  \n\n"
    character_memories.load_memories.return_value = memories
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    player_data_for_prompt = factory.create_player_data_for_prompt()
    assert player_data_for_prompt.get_player_memories() == ["Memory1", "Memory2"]


def test_player_data_for_prompt_factory_create_player_data_for_prompt_empty_memory_value():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    player_identifier = "Player1"
    playthrough_manager.get_player_identifier.return_value = player_identifier
    player = Mock()
    player.name = "TestPlayer"
    player.description = "A brave warrior"
    player.personality = "Bold and fearless"
    player.profile = "Profile info"
    player.likes = "Adventure"
    player.dislikes = "Cowardice"
    player.secrets = "Secret identity"
    player.speech_patterns = "Speaks with confidence"
    player.health = 100
    player.equipment = "Sword and shield"
    character_factory.create_character.return_value = player
    memories = ""
    character_memories.load_memories.return_value = memories
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    player_data_for_prompt = factory.create_player_data_for_prompt()
    assert player_data_for_prompt.get_player_memories() == []


def test_player_data_for_prompt_factory_create_player_data_for_prompt_with_missing_player_attributes():
    playthrough_name = "TestPlaythrough"
    character_factory = Mock(spec=CharacterFactory)
    playthrough_manager = Mock(spec=PlaythroughManager)
    character_memories = Mock(spec=CharacterMemoriesManager)
    player_identifier = "Player1"
    playthrough_manager.get_player_identifier.return_value = player_identifier
    player = Mock()
    player.name = None
    player.description = ""
    player.personality = None
    player.profile = ""
    player.likes = None
    player.dislikes = ""
    player.secrets = None
    player.speech_patterns = ""
    player.health = None
    player.equipment = ""
    character_factory.create_character.return_value = player
    character_memories.load_memories.return_value = None
    factory = PlayerDataForPromptFactory(
        playthrough_name,
        character_factory,
        playthrough_manager=playthrough_manager,
        character_memories=character_memories,
    )
    player_data_for_prompt = factory.create_player_data_for_prompt()
    expected_player_data = {
        "player_name": player.name,
        "player_description": player.description,
        "player_personality": player.personality,
        "player_profile": player.profile,
        "player_likes": player.likes,
        "player_dislikes": player.dislikes,
        "player_secrets": player.secrets,
        "player_speech_patterns": player.speech_patterns,
        "player_health": player.health,
        "player_equipment": player.equipment,
    }
    assert player_data_for_prompt.get_player_data_for_prompt() == expected_player_data
    assert player_data_for_prompt.get_player_memories() == []
