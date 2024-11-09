from typing import List, Optional, Dict, Any

from src.base.validators import validate_non_empty_string
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)


class LoadDataFromOngoingDialogueAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        dialogue_participants_identifiers: Optional[List[str]],
        purpose: Optional[str],
        has_ongoing_dialogue: bool,
        ongoing_dialogue_repository: Optional[OngoingDialogueRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._dialogue_participants_identifiers = dialogue_participants_identifiers
        self._purpose = purpose
        self._has_ongoing_dialogue = has_ongoing_dialogue

        self._ongoing_dialogue_repository = (
            ongoing_dialogue_repository
            or OngoingDialogueRepository(self._playthrough_name)
        )

    def do_algorithm(self) -> Dict[str, Any]:
        data = {}

        if self._has_ongoing_dialogue and (
            not self._dialogue_participants_identifiers or not self._purpose
        ):
            self._ongoing_dialogue_repository.validate_dialogue_is_not_malformed()

            # At this point, the necessary data is present in the loaded ongoing dialogue file.
            if not self._dialogue_participants_identifiers:
                data["participants"] = (
                    self._ongoing_dialogue_repository.get_participants()
                )
            if not self._purpose:
                data["purpose"] = self._ongoing_dialogue_repository.get_purpose()

        return data
