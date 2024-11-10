from src.base.validators import validate_non_empty_string
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.providers.grow_event_provider import GrowEventProvider
from src.dialogues.transcription import Transcription
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class GrowEventProviderFactory:
    def __init__(
        self,
        suggested_event: str,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
    ):
        validate_non_empty_string(suggested_event, "suggested_event")

        self._suggested_event = suggested_event
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

    def create_provider(self, transcription: Transcription) -> GrowEventProvider:
        return GrowEventProvider(
            self._suggested_event,
            transcription,
            self._format_known_facts_algorithm,
            self._produce_tool_response_strategy_factory,
            self._local_information_factory,
            self._relevant_characters_information_factory,
        )
