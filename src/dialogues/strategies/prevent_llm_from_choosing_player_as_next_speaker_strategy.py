import logging
import random

from src.dialogues.participants import Participants
from src.playthrough_manager import PlaythroughManager

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
        if (
            self._playthrough_manager.get_player_identifier()
            == function_call_arguments["identifier"]
        ):
            logger.warning(
                f"The LLM chose the player as the next speaking turn choice: %s",
                function_call_arguments,
            )

            # Change the "identifier" in function_call_arguments to any random participant in self._participants.get() that isn't the player.
            participant_keys = self._participants.get_participant_keys()

            # Remove the player's identifier from the participant keys
            participant_keys.remove(self._playthrough_manager.get_player_identifier())

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
            else:
                # this should never happen
                raise ValueError("No other participants available besides the player.")

        return function_call_arguments
