import logging
from typing import List, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.dialogues.algorithms.extract_identifiers_from_participants_data_algorithm import (
    ExtractIdentifiersFromParticipantsDataAlgorithm,
)
from src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm import (
    LoadDataFromOngoingDialogueAlgorithm,
)
from src.dialogues.enums import HandleDialogueStateAlgorithmResultType
from src.dialogues.products.handle_dialogue_state_algorithm_product import (
    HandleDialogueStateAlgorithmProduct,
)

logger = logging.getLogger(__name__)


class HandleDialogueStateDirector:
    def __init__(
        self,
        playthrough_name: str,
        dialogue_participant_identifiers: Optional[List[str]],
        load_data_from_ongoing_dialogue_algorithm: LoadDataFromOngoingDialogueAlgorithm,
        extract_identifiers_from_participants_data_algorithm: ExtractIdentifiersFromParticipantsDataAlgorithm,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._dialogue_participant_identifiers = dialogue_participant_identifiers
        self._load_data_from_ongoing_dialogue_algorithm = (
            load_data_from_ongoing_dialogue_algorithm
        )
        self._extract_identifiers_from_participants_data_algorithm = (
            extract_identifiers_from_participants_data_algorithm
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def direct(self) -> HandleDialogueStateAlgorithmProduct:
        has_ongoing_dialogue = self._playthrough_manager.has_ongoing_dialogue()

        if not self._dialogue_participant_identifiers and not has_ongoing_dialogue:
            logger.info("There were no dialogue participants, and no ongoing dialogue.")
            return HandleDialogueStateAlgorithmProduct(
                None,
                HandleDialogueStateAlgorithmResultType.SHOULD_REDIRECT_TO_PARTICIPANTS,
            )

        # At this point we either have dialogue identifiers or an ongoing dialogue.
        data = self._load_data_from_ongoing_dialogue_algorithm.do_algorithm()

        # If at this point we still don't have data, then either we have the participants on session,
        # or there isn't an ongoing conversation either.
        if not self._dialogue_participant_identifiers and not data:
            return HandleDialogueStateAlgorithmProduct(
                data,
                HandleDialogueStateAlgorithmResultType.SHOULD_REDIRECT_TO_PARTICIPANTS,
            )

        data = self._extract_identifiers_from_participants_data_algorithm.do_algorithm(
            data
        )

        return HandleDialogueStateAlgorithmProduct(
            data, HandleDialogueStateAlgorithmResultType.CONTINUE
        )
