import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.tools import join_with_newline
from src.base.validators import validate_non_empty_string
from src.dialogues.configs.llm_speech_data_provider_algorithms_config import (
    LlmSpeechDataProviderAlgorithmsConfig,
)
from src.dialogues.configs.llm_speech_data_provider_config import (
    LlmSpeechDataProviderConfig,
)
from src.dialogues.configs.llm_speech_data_provider_factories_config import (
    LlmSpeechDataProviderFactoriesConfig,
)
from src.dialogues.products.concrete_speech_data_product import (
    ConcreteSpeechDataProduct,
)
from src.filesystem.path_manager import PathManager
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class LlmSpeechDataProvider(BaseToolResponseProvider):
    def __init__(
        self,
        config: LlmSpeechDataProviderConfig,
        factories_config: LlmSpeechDataProviderFactoriesConfig,
        algorithms_config: LlmSpeechDataProviderAlgorithmsConfig,
        time_manager: Optional[TimeManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory,
            path_manager,
        )

        validate_non_empty_string(config.playthrough_name, "playthrough_name")
        validate_non_empty_string(config.speaker_name, "speaker_name")

        self._config = config
        self._factories_config = factories_config
        self._algorithms_config = algorithms_config

        self._time_manager = time_manager or TimeManager(self._config.playthrough_name)

    def _format_participant_details(self) -> str:
        return "\n".join(
            [
                f"{participant['name']}: {participant['description']}. Equipment: {participant['equipment']}. Health: {participant['health']}."
                for _, participant in self._config.participants.get().items()
                if participant["name"] != self._config.speaker_name
            ]
        )

    def _format_dialogue_purpose(self) -> str:
        if self._config.purpose:
            return f"General Purpose of the Dialogue: {self._config.purpose}"
        return ""

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_speech_turn_prompt_path()

    def get_user_content(self) -> str:
        return f"Write {self._config.speaker_name}'s speech."

    def create_product_from_base_model(self, response_model: BaseModel):
        speech_data = {
            "name": response_model.name,
            "narration_text": response_model.narration_text,
            "speech": response_model.speech,
            "thoughts": response_model.thoughts,
            "desired_action": response_model.desired_action,
        }

        return ConcreteSpeechDataProduct(speech_data, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        places_descriptions = (
            self._factories_config.places_descriptions_provider.get_information()
        )

        participant_details = self._format_participant_details()

        dialogue_purpose = self._format_dialogue_purpose()

        character_dialogue_purpose = (
            self._algorithms_config.format_character_dialogue_purpose_algorithm.do_algorithm()
        )

        transcription = self._config.transcription.get_prettified_transcription()

        known_facts = self._algorithms_config.format_known_facts_algorithm.do_algorithm(
            join_with_newline(
                places_descriptions,
                participant_details,
                dialogue_purpose,
                character_dialogue_purpose,
                transcription,
            )
        )

        character_information = self._factories_config.character_information_provider_factory.create_provider(
            join_with_newline(
                places_descriptions,
                participant_details,
                dialogue_purpose,
                character_dialogue_purpose,
                transcription,
                known_facts,
            ),
            use_interview=True,
        ).get_information()

        return {
            "places_descriptions": places_descriptions,
            "hour": self._time_manager.get_hour(),
            "time_group": self._time_manager.get_time_of_the_day(),
            "name": self._config.speaker_name,
            "participant_details": participant_details,
            "character_information": character_information,
            "known_facts": known_facts,
            "dialogue_purpose": dialogue_purpose,
            "character_dialogue_purpose": character_dialogue_purpose,
            "transcription_excerpt": self._config.transcription.get_transcription_excerpt(),
        }
