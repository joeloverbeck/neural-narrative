from typing import Dict, List

from src.base.required_string import RequiredString


class PlayerDataForPrompt:
    def __init__(
        self,
        player_data_for_prompt: Dict[str, RequiredString],
        player_memories: List[RequiredString],
    ):
        if (
            "memories" in player_data_for_prompt
            or "player_memories" in player_data_for_prompt
        ):
            raise ValueError(
                "Found 'memories' in player_data_for_prompt. This class is meant to be used for cased where memory is going to be combined."
            )

        self._player_data_for_prompt = player_data_for_prompt
        self._player_memories = player_memories

    def get_player_data_for_prompt(self) -> Dict[str, RequiredString]:
        return self._player_data_for_prompt

    def get_player_memories(self) -> List[RequiredString]:
        return self._player_memories
