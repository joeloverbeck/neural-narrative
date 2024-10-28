from typing import List, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy


class FollowersIdentifiersStrategy(OtherCharactersIdentifiersStrategy):
    def __init__(
        self,
        playthrough_name: str,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def get_data(self) -> List[str]:
        return self._playthrough_manager.get_followers()
