from typing import Optional, List

from src.characters.characters_manager import CharactersManager
from src.playthrough_manager import PlaythroughManager


class PartyDataForPromptFactory:
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

    def _get_followers_data(self) -> List[dict]:
        follower_ids = self._playthrough_manager.get_followers()
        return self._characters_manager.get_full_data_of_characters(follower_ids)

    def _get_followers_information(self) -> str:
        followers_info = ""

        for follower in self._get_followers_data():
            followers_info += (
                f"- Follower name: {follower['name']}\n"
                f"- Description: {follower['description']}\n"
                f"- Personality: {follower['personality']}\n"
                f"- Profile: {follower['profile']}\n"
                f"- Likes: {follower['likes']}\n"
                f"- Dislikes: {follower['dislikes']}\n"
                f"- Speech patterns: {follower['speech patterns']}\n"
                f"- Equipment: {follower['equipment']}\n-----\n"
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
        player_data["memories"] = player_memories

        # Get followers data and their memories
        followers_data = self._get_followers_information()

        followers_memories = self._get_followers_memories()

        combined_memories = self._get_combined_memories(
            player_memories, followers_memories
        )

        return {
            "player_name": player_data["name"],
            "player_description": player_data["description"],
            "player_personality": player_data["personality"],
            "player_profile": player_data["profile"],
            "player_likes": player_data["likes"],
            "player_dislikes": player_data["dislikes"],
            "player_speech_patterns": player_data["speech patterns"],
            "player_equipment": player_data["equipment"],
            "followers_information": followers_data,
            "combined_memories": combined_memories,
        }

    def _get_followers_memories(self):
        # Combine memories from player and followers, removing duplicates
        followers_memories = []

        for follower in self._get_followers_data():
            memories_str = self._characters_manager.load_character_memories(
                follower["identifier"]
            )
            # Convert the memories string into a list
            memories_list = [
                memory.strip()
                for memory in memories_str.strip().split("\n")
                if memory.strip()
            ]
            followers_memories.extend(memories_list)

        return followers_memories
