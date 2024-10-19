import logging
import random

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.participants import Participants

logger = logging.getLogger(__name__)


class PreventLlmFromChoosingPlayerAsNextSpeakerStrategy:
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        playthrough_manager: PlaythroughManager = None,
    ):

        self._playthrough_name = playthrough_name
        self._participants = participants

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def prevent_llm_from_choosing_player(self, function_call_arguments: dict) -> dict:
        if not self._participants.enough_participants():
            raise ValueError(
                f"There weren't enough participants for the dialogue to begin with: {self._participants.number_of_participants()}"
            )

        player_identifier_str = str(self._playthrough_manager.get_player_identifier())
        function_identifier_str = str(function_call_arguments["identifier"])

        if player_identifier_str == function_identifier_str:
            participant_keys = self._participants.get_participant_keys()

            # Remove the player's identifier from the participant keys
            participant_keys = [
                str(k) for k in participant_keys if str(k) != player_identifier_str
            ]

            if participant_keys:
                # Select a random participant that is not the player
                random_identifier = random.choice(participant_keys)
                function_call_arguments["identifier"] = random_identifier
                function_call_arguments["name"] = self._participants.get()[
                    random_identifier
                ]["name"]
                function_call_arguments["reason"] = (
                    "The LLM incorrectly chose the player as the next speaking choice."
                )
                logger.info(
                    "New character chosen for next speaking part instead of the player: (%s) %s.",
                    function_call_arguments["identifier"],
                    function_call_arguments["name"],
                )
            else:
                # this should never happen
                raise ValueError("No other participants available besides the player.")

        return function_call_arguments
