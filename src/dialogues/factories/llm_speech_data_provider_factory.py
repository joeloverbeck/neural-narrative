from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.dialogues.configs.llm_speech_data_provider_config import (
    LlmSpeechDataProviderConfig,
)
from src.dialogues.configs.llm_speech_data_provider_factories_config import (
    LlmSpeechDataProviderFactoriesConfig,
)
from src.dialogues.participants import Participants
from src.dialogues.providers.llm_speech_data_provider import LlmSpeechDataProvider
from src.dialogues.transcription import Transcription
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class LlmSpeechDataProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        purpose: Optional[str],
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_provider: PlacesDescriptionsProvider,
        character_information_provider_factory: CharacterInformationProviderFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._places_descriptions_provider = places_descriptions_provider
        self._character_information_provider_factory = (
            character_information_provider_factory
        )

    def create_llm_speech_data_provider(
        self, speaker_identifier: str, speaker_name: str, transcription: Transcription
    ) -> LlmSpeechDataProvider:
        validate_non_empty_string(speaker_name, "speaker_name")
        return LlmSpeechDataProvider(
            LlmSpeechDataProviderConfig(
                self._playthrough_name,
                speaker_identifier,
                speaker_name,
                self._participants,
                self._purpose,
                transcription,
            ),
            LlmSpeechDataProviderFactoriesConfig(
                self._produce_tool_response_strategy_factory,
                self._places_descriptions_provider,
                self._character_information_provider_factory,
            ),
        )
