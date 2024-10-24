import logging
from typing import Optional

from pydantic import BaseModel

from src.base.constants import CHOOSING_SPEECH_TURN_PROMPT_FILE
from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class SpeechTurnChoiceToolResponseProvider(BaseToolResponseProvider):
    def __init__(
        self,
        player_identifier: str,
        participants: Participants,
        transcription: Transcription,
        character_factory: CharacterFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        validate_non_empty_string(player_identifier, "player_identifier")

        self._player_identifier = player_identifier
        self._participants = participants
        self._transcription = transcription
        self._character_factory = character_factory

    def get_prompt_file(self) -> str:
        return CHOOSING_SPEECH_TURN_PROMPT_FILE

    def get_user_content(self) -> str:
        return "Choose who will speak next in this dialogue. Choose only among the allowed participants."

    def create_product_from_base_model(self, response_model: BaseModel):
        llm_response = {
            "identifier": str(response_model.identifier),
            "name": response_model.name,
            "reason": response_model.reason,
        }

        # The system requires to include the "voice_model" into the llm_response.
        character = self._character_factory.create_character(llm_response["identifier"])

        llm_response.update({"voice_model": character.voice_model})

        return ConcreteLlmToolResponseProduct(llm_response, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        all_participants = "\n".join(
            [
                f"Identifier: {identifier} / Name: {participant['name']}"
                for identifier, participant in self._participants.get().items()
            ]
        )
        if self._player_identifier:
            participants_without_player = "\n".join(
                [
                    f"Identifier: {identifier} / Name: {participant['name']} / Personality: {participant['personality']}"
                    for identifier, participant in self._participants.get().items()
                    if identifier != self._player_identifier
                ]
            )
        else:
            participants_without_player = all_participants

        return {
            "all_participants": all_participants,
            "dialogue": self._transcription.get(),
            "participants_without_player": participants_without_player,
        }
