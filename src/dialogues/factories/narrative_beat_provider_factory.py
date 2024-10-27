from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
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
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._local_information_factory = local_information_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def create_provider(self, transcription: Transcription) -> NarrativeBeatProvider:
        return NarrativeBeatProvider(
            transcription,
            self._produce_tool_response_strategy_factory,
            self._local_information_factory,
            self._player_and_followers_information_factory,
        )
