import logging
from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    DIALOGUE_PROMPT_FILE,
)
from src.base.validators import validate_non_empty_string
from src.dialogues.configs.llm_speech_data_provider_config import (
    LlmSpeechDataProviderConfig,
)
from src.dialogues.configs.llm_speech_data_provider_factories_config import (
    LlmSpeechDataProviderFactoriesConfig,
)
from src.dialogues.products.concrete_speech_data_product import (
    ConcreteSpeechDataProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class LlmSpeechDataProvider(BaseToolResponseProvider):
    def __init__(
        self,
        config: LlmSpeechDataProviderConfig,
        factories_config: LlmSpeechDataProviderFactoriesConfig,
        time_manager: Optional[TimeManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory, filesystem_manager
        )

        validate_non_empty_string(config.playthrough_name, "playthrough_name")
        validate_non_empty_string(config.speaker_identifier, "speaker_identifier")
        validate_non_empty_string(config.speaker_name, "speaker_name")

        self._config = config
        self._factories_config = factories_config

        self._time_manager = time_manager or TimeManager(self._config.playthrough_name)

    def _format_participant_details(self) -> str:
        return "\n".join(
            [
                f"{participant['name']}: {participant['description']}. Equipment: {participant['equipment']}"
                for _, participant in self._config.participants.get().items()
                if participant["name"] != self._config.speaker_name
            ]
        )

    def _format_dialogue_purpose(self) -> str:
        if self._config.purpose:
            return f"The purpose of this dialogue is: {self._config.purpose}"
        return ""

    def get_prompt_file(self) -> str:
        return DIALOGUE_PROMPT_FILE

    def get_user_content(self) -> str:
        return f"Write {self._config.speaker_name}'s speech."

    def create_product_from_base_model(self, response_model: BaseModel):
        # The base model is a MaybeSpeechTurn, given that it fails somewhat often.
        if response_model.result is not None:
            speech_data_response = response_model.result

            speech_data = {
                "name": speech_data_response.name,
                "narration_text": speech_data_response.narration_text,
                "speech": speech_data_response.speech.speech,
            }

            return ConcreteSpeechDataProduct(speech_data, is_valid=True)

        # The call failed.
        return ConcreteSpeechDataProduct(
            None, is_valid=False, error=response_model.message
        )

    def get_prompt_kwargs(self) -> dict:
        participant_details = self._format_participant_details()
        dialogue_purpose = self._format_dialogue_purpose()

        return {
            "places_descriptions": self._factories_config.places_descriptions_provider.get_information(),
            "hour": self._time_manager.get_hour(),
            "time_group": self._time_manager.get_time_of_the_day(),
            "name": self._config.speaker_name,
            "participant_details": participant_details,
            "character_information": self._factories_config.character_information_provider_factory.create_provider(
                self._config.speaker_identifier
            ).get_information(),
            "dialogue_purpose": dialogue_purpose,
            "dialogue": self._config.transcription.get_prettified_transcription(),
        }
