from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.exceptions import InvalidNextSpeakerError
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)


class DetermineNextSpeakerAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        transcription: Transcription,
        speech_turn_choice_tool_response_provider_factory: SpeechTurnChoiceToolResponseProviderFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not participants.enough_participants():
            raise ValueError(
                f"There weren't enough participants for a dialogue. {participants.get()}"
            )

        self._participants = participants
        self._transcription = transcription
        self._speech_turn_choice_tool_response_provider_factory = (
            speech_turn_choice_tool_response_provider_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def _choose_next_speaker(self) -> LlmToolResponseProduct:
        """Determine the next speaker in the dialogue."""
        response_provider = (
            self._speech_turn_choice_tool_response_provider_factory.create_provider(
                self._transcription
            )
        )
        response_product = response_provider.generate_product()

        if not response_product.is_valid():
            raise InvalidNextSpeakerError(response_product.get_error())

        return response_product

    def _determine_next_speaker(self) -> LlmToolResponseProduct:
        if self._participants.has_only_two_participants_with_player(
            self._playthrough_manager.get_player_identifier()
        ):
            return ConcreteLlmToolResponseProduct(
                self._participants.get_other_participant_data(
                    self._playthrough_manager.get_player_identifier()
                ),
                is_valid=True,
            )

        # There are more than two participants, so we must delegate choosing the next speaker.
        return self._choose_next_speaker()

    def _validate_next_speaker(
        self, speech_turn_choice_response: LlmToolResponseProduct
    ) -> None:
        """Validate that the next speaker is not the player."""
        if "voice_model" not in speech_turn_choice_response.get():
            raise ValueError("voice_model can't be empty.")
        if (
            speech_turn_choice_response.get()["identifier"]
            == self._playthrough_manager.get_player_identifier()
        ):
            raise InvalidNextSpeakerError("Next speaker cannot be the player.")

    def do_algorithm(self) -> LlmToolResponseProduct:
        speech_turn_choice_response = self._determine_next_speaker()

        self._validate_next_speaker(speech_turn_choice_response)

        return speech_turn_choice_response
