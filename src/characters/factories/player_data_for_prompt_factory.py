from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.characters.products.player_data_for_prompt import PlayerDataForPrompt


class PlayerDataForPromptFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_factory: CharacterFactory,
        retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._character_factory = character_factory
        self._retrieve_memories_algorithm_factory = retrieve_memories_algorithm_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def create_player_data_for_prompt(self, query_text: str) -> PlayerDataForPrompt:
        validate_non_empty_string(query_text, "query_text")

        player_identifier = self._playthrough_manager.get_player_identifier()

        player_memories = self._retrieve_memories_algorithm_factory.create_algorithm(
            player_identifier, query_text
        ).do_algorithm()

        player = self._character_factory.create_character(player_identifier)

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
