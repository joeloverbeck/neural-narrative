from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.dialogues.factories.format_character_dialogue_purpose_algorithm_factory import (
    FormatCharacterDialoguePurposeAlgorithmFactory,
)
from src.dialogues.factories.llm_speech_data_provider_factory import (
    LlmSpeechDataProviderFactory,
)
from src.dialogues.participants import Participants
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class LlmSpeechDataProviderFactoryComposer:

    def __init__(
        self, playthrough_name: str, participants: Participants, purpose: Optional[str]
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose

    def compose(self) -> LlmSpeechDataProviderFactory:
        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_speech_turn(),
            ).compose_factory()
        )

        places_descriptions_provider = PlacesDescriptionsProviderComposer(
            self._playthrough_name
        ).compose_provider()

        character_information_provider_factory = CharacterInformationProviderFactory(
            self._playthrough_name
        )

        format_character_dialogue_purpose_algorithm_factory = (
            FormatCharacterDialoguePurposeAlgorithmFactory(self._playthrough_name)
        )

        return LlmSpeechDataProviderFactory(
            self._playthrough_name,
            self._participants,
            self._purpose,
            format_character_dialogue_purpose_algorithm_factory,
            produce_tool_response_strategy_factory,
            places_descriptions_provider,
            character_information_provider_factory,
        )
