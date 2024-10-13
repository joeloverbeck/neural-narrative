from typing import Optional

from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.characters.products.player_data_for_prompt import PlayerDataForPrompt
from src.playthrough_manager import PlaythroughManager


class PlayerDataForPromptFactory:
    def __init__(
        self,
        playthrough_name: str,
        playthrough_manager: Optional[PlaythroughManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._character_memories = character_memories or CharacterMemories(
            self._playthrough_name
        )

    def create_player_data_for_prompt(self) -> PlayerDataForPrompt:
        player_identifier = self._playthrough_manager.get_player_identifier()
        player = Character(self._playthrough_name, player_identifier)

        # Load and process the player's memories
        memories_str = self._character_memories.load_memories(player)

        player_memories = [
            memory.strip()
            for memory in memories_str.strip().split("\n")
            if memory.strip()
        ]

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
