from src.base.required_string import RequiredString
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import (
    DetermineUserMessagesForSpeechTurnStrategy,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.strategies.concrete_determine_user_messages_for_speech_turn_strategy import (
    ConcreteDetermineUserMessagesForSpeechTurnStrategy,
)


class DetermineUserMessagesForSpeechTurnStrategyFactory:
    def __init__(
            self, playthrough_name: RequiredString, player_identifier: RequiredString
    ):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier

    def create_strategy(
        self, player_input_product: PlayerInputProduct, messages_to_llm: MessagesToLlm
    ) -> DetermineUserMessagesForSpeechTurnStrategy:
        return ConcreteDetermineUserMessagesForSpeechTurnStrategy(
            self._playthrough_name,
            self._player_identifier,
            player_input_product,
            messages_to_llm,
        )
