from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_memories import CharacterMemories
from src.characters.factories.character_factory import CharacterFactory
from src.characters.products.player_data_for_prompt import PlayerDataForPrompt


class PlayerDataForPromptFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_factory: CharacterFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        self._character_factory = character_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._character_memories = character_memories or CharacterMemories(
            playthrough_name
        )

    def create_player_data_for_prompt(self) -> PlayerDataForPrompt:
        player_identifier = self._playthrough_manager.get_player_identifier()
        player = self._character_factory.create_character(player_identifier)
        memories = self._character_memories.load_memories(player)
        if memories:
            player_memories = [
                memory.strip()
                for memory in memories.strip().split("\n")
                if memory.strip()
            ]
        else:
            player_memories = []
        return PlayerDataForPrompt(
            {
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
            },
            player_memories,
        )
