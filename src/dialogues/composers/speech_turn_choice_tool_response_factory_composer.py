from src.characters.factories.character_factory import CharacterFactory
from src.dialogues.participants import Participants
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import (
    SpeechTurnChoiceToolResponseProviderFactory,
)
from src.prompting.llms import Llms


class SpeechTurnChoiceToolResponseFactoryComposer:

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants

    def compose(self) -> SpeechTurnChoiceToolResponseProviderFactory:
        character_factory = CharacterFactory(self._playthrough_name)

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_speech_turn_choice(),
            ).compose_factory()
        )

        return SpeechTurnChoiceToolResponseProviderFactory(
            self._playthrough_name,
            self._player_identifier,
            self._participants,
            character_factory,
            produce_tool_response_strategy_factory,
        )
