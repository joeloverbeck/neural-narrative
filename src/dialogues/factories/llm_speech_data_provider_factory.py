from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.composers.character_information_provider_factory_composer import (
    CharacterInformationProviderFactoryComposer,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.configs.llm_speech_data_provider_algorithms_config import (
    LlmSpeechDataProviderAlgorithmsConfig,
)
from src.dialogues.configs.llm_speech_data_provider_config import (
    LlmSpeechDataProviderConfig,
)
from src.dialogues.configs.llm_speech_data_provider_factories_config import (
    LlmSpeechDataProviderFactoriesConfig,
)
from src.dialogues.factories.format_character_dialogue_purpose_algorithm_factory import (
    FormatCharacterDialoguePurposeAlgorithmFactory,
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
        format_character_dialogue_purpose_algorithm_factory: FormatCharacterDialoguePurposeAlgorithmFactory,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_provider: PlacesDescriptionsProvider,
        character_information_provider_factory_composer: CharacterInformationProviderFactoryComposer,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._format_character_dialogue_purpose_algorithm_factory = (
            format_character_dialogue_purpose_algorithm_factory
        )
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._places_descriptions_provider = places_descriptions_provider
        self._character_information_provider_factory_composer = (
            character_information_provider_factory_composer
        )

    def create_llm_speech_data_provider(
        self,
        speaker_identifier: str,
        speaker_name: str,
        transcription: Transcription,
    ) -> LlmSpeechDataProvider:
        validate_non_empty_string(speaker_name, "speaker_name")
        return LlmSpeechDataProvider(
            LlmSpeechDataProviderConfig(
                self._playthrough_name,
                speaker_name,
                self._participants,
                self._purpose,
                transcription,
            ),
            LlmSpeechDataProviderFactoriesConfig(
                self._produce_tool_response_strategy_factory,
                self._places_descriptions_provider,
                self._character_information_provider_factory_composer.compose_factory(
                    speaker_identifier
                ),
            ),
            LlmSpeechDataProviderAlgorithmsConfig(
                self._format_character_dialogue_purpose_algorithm_factory.create_algorithm(
                    speaker_identifier, speaker_name
                ),
                self._format_known_facts_algorithm,
            ),
        )
