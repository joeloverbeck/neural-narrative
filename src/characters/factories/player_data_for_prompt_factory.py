from typing import Optional

from src.characters.characters_manager import CharactersManager
from src.characters.products.player_data_for_prompt import PlayerDataForPrompt
from src.playthrough_manager import PlaythroughManager


class PlayerDataForPromptFactory:
    def __init__(
        self,
        playthrough_name: str,
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def create_player_data_for_prompt(self) -> PlayerDataForPrompt:
        player_identifier = self._playthrough_manager.get_player_identifier()
        player_data = self._characters_manager.load_character_data(player_identifier)

        # Load and process the player's memories
        memories_str = self._characters_manager.load_character_memories(
            player_identifier
        )
        player_memories = [
            memory.strip()
            for memory in memories_str.strip().split("\n")
            if memory.strip()
        ]

        return PlayerDataForPrompt(
            {
                "player_name": player_data["name"],
                "player_description": player_data["description"],
                "player_personality": player_data["personality"],
                "player_profile": player_data["profile"],
                "player_likes": player_data["likes"],
                "player_dislikes": player_data["dislikes"],
                "player_speech_patterns": player_data["speech patterns"],
                "player_health": player_data["health"],
                "player_equipment": player_data["equipment"],
            },
            player_memories,
        )
