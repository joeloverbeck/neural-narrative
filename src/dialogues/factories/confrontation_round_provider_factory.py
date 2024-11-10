from src.base.validators import validate_non_empty_string
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.providers.confrontation_round_provider import (
    ConfrontationRoundProvider,
)
from src.dialogues.transcription import Transcription
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class ConfrontationRoundProviderFactory:
    def __init__(
        self,
        playthrough_name: str,
        confrontation_context: str,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(confrontation_context, "confrontation_context")

        self._playthrough_name = playthrough_name
        self._confrontation_context = confrontation_context
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

    def create_provider(
        self, transcription: Transcription
    ) -> ConfrontationRoundProvider:
        return ConfrontationRoundProvider(
            self._playthrough_name,
            self._confrontation_context,
            transcription,
            self._format_known_facts_algorithm,
            self._produce_tool_response_strategy_factory,
            self._local_information_factory,
            self._relevant_characters_information_factory,
        )
