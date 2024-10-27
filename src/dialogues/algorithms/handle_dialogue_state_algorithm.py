import logging
from typing import List, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.dialogues.products.handle_dialogue_state_algorithm_product import (
    HandleDialogueStateAlgorithmProduct,
)
from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class HandleDialogueStateAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        dialogue_participant_identifiers: Optional[List[str]],
        purpose: Optional[str],
        playthrough_manager: Optional[PlaythroughManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._dialogue_participant_identifiers = dialogue_participant_identifiers
        self._purpose = purpose

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> HandleDialogueStateAlgorithmProduct:
        has_ongoing_dialogue = self._playthrough_manager.has_ongoing_dialogue(
            self._playthrough_name
        )

        if not self._dialogue_participant_identifiers and not has_ongoing_dialogue:
            logger.info("There were no dialogue participants, and no ongoing dialogue.")
            return HandleDialogueStateAlgorithmProduct(None)

        data = {}

        if has_ongoing_dialogue and (
            not self._dialogue_participant_identifiers or not self._purpose
        ):
            ongoing_dialogue_file = read_json_file(
                self._path_manager.get_ongoing_dialogue_path(self._playthrough_name)
            )

            if (
                not "participants" in ongoing_dialogue_file
                or not "purpose" in ongoing_dialogue_file
            ):
                raise ValueError(
                    f"Malformed ongoing dialogue file: {ongoing_dialogue_file}"
                )

            if not self._dialogue_participant_identifiers:
                data["participants"] = ongoing_dialogue_file.get("participants")
            if not self._purpose:
                data["purpose"] = ongoing_dialogue_file.get("purpose")

        return HandleDialogueStateAlgorithmProduct(data)
