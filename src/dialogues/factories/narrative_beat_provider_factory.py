from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.providers.narrative_beat_provider import NarrativeBeatProvider
from src.dialogues.transcription import Transcription
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class NarrativeBeatProviderFactory:
    def __init__(
        self,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
    ):
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

    def create_provider(self, transcription: Transcription) -> NarrativeBeatProvider:
        return NarrativeBeatProvider(
            transcription,
            self._format_known_facts_algorithm,
            self._produce_tool_response_strategy_factory,
            self._local_information_factory,
            self._relevant_characters_information_factory,
        )
