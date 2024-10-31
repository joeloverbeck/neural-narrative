from typing import Any, Dict, List, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string


class ExtractIdentifiersFromParticipantsDataAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        dialogue_participants_identifiers: List[str],
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._dialogue_participants_identifiers = dialogue_participants_identifiers

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def do_algorithm(self, data: Dict[str, Any]) -> Dict[str, Any]:
        dialogue_participants: List[str] = (
            self._dialogue_participants_identifiers
            if self._dialogue_participants_identifiers
            else []
        )

        # Now it's when we determine if we have data but not participants on session.
        if not dialogue_participants and data:
            player_identifier = self._playthrough_manager.get_player_identifier()

            for key in data.get("participants").keys():
                if key != player_identifier:
                    dialogue_participants.append(key)
        data["participants"] = dialogue_participants

        return data
