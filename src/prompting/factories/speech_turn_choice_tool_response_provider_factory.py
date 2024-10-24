from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.speech_turn_tool_response_provider import (
    SpeechTurnChoiceToolResponseProvider,
)


class SpeechTurnChoiceToolResponseProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        character_factory: CharacterFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._character_factory = character_factory
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(
        self, transcription: Transcription
    ) -> SpeechTurnChoiceToolResponseProvider:
        return SpeechTurnChoiceToolResponseProvider(
            self._player_identifier,
            self._participants,
            transcription,
            self._character_factory,
            self._produce_tool_response_strategy_factory,
        )
