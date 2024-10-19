from typing import Optional, List

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.characters.characters_manager import CharactersManager
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


class PartyDataForPromptFactory:
    def __init__(
        self,
        playthrough_name: str,
        player_data_for_prompt_factory: PlayerDataForPromptFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._player_data_for_prompt_factory = player_data_for_prompt_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._character_memories = character_memories or CharacterMemories(
            self._playthrough_name
        )

    def _get_followers_data(self) -> List[Character]:
        follower_ids = self._playthrough_manager.get_followers()
        return self._characters_manager.get_characters(follower_ids)

    def _get_followers_information(self) -> str:
        followers_info = ""

        for follower in self._get_followers_data():
            followers_info += (
                f"- Follower name: {follower.name}\n"
                f"- Description: {follower.description}\n"
                f"- Personality: {follower.personality}\n"
                f"- Profile: {follower.profile}\n"
                f"- Likes: {follower.likes}\n"
                f"- Dislikes: {follower.dislikes}\n"
                f"- Speech patterns: {follower.speech_patterns}\n"
                f"- Equipment: {follower.equipment}\n-----\n"
            )

        return followers_info

    @staticmethod
    def _get_combined_memories(
        player_memories: List[str], followers_memories: List[str]
    ) -> List[str]:
        all_memories = player_memories.copy()

        all_memories.extend(followers_memories)

        # Remove duplicates while preserving order
        seen = set()
        unique_memories = []
        for memory in all_memories:
            if memory not in seen:
                seen.add(memory)
                unique_memories.append(memory)
        return unique_memories

    def get_party_data_for_prompt(self) -> dict:
        player_data_for_prompt = (
            self._player_data_for_prompt_factory.create_player_data_for_prompt()
        )

        # Get followers data and their memories
        followers_data = self._get_followers_information()

        followers_memories = self._get_followers_memories()

        combined_memories = self._get_combined_memories(
            player_data_for_prompt.get_player_memories(), followers_memories
        )

        data_for_prompt = player_data_for_prompt.get_player_data_for_prompt()

        data_for_prompt.update(
            {
                "followers_information": followers_data,
                "combined_memories": combined_memories,
            }
        )

        return data_for_prompt

    def _get_followers_memories(self):
        # Combine memories from player and followers, removing duplicates
        followers_memories = []

        for follower in self._get_followers_data():
            memories_str = self._character_memories.load_memories(follower)

            # Convert the memories string into a list
            memories_list = [
                memory.strip()
                for memory in memories_str.strip().split("\n")
                if memory.strip()
            ]
            followers_memories.extend(memories_list)

        return followers_memories
