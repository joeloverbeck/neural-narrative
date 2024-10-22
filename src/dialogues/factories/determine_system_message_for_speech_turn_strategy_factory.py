from src.dialogues.abstracts.strategies import (
    DetermineSystemMessageForSpeechTurnStrategy,
)
from src.dialogues.factories.dialogue_initial_prompting_messages_provider_factory import (
    DialogueInitialPromptingMessagesProviderFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.strategies.concrete_determine_system_message_for_speech_turn_strategy import (
    ConcreteDetermineSystemMessageForSpeechTurnStrategy,
)


class DetermineSystemMessageForSpeechTurnStrategyFactory:

    def __init__(
        self,
        dialogue_initial_prompting_messages_provider_factory: DialogueInitialPromptingMessagesProviderFactory,
    ):
        self._dialogue_initial_prompting_messages_provider_factory = (
            dialogue_initial_prompting_messages_provider_factory
        )

    def create_determine_system_message_for_speech_turn_strategy(
        self, messages_to_llm: MessagesToLlm
    ) -> DetermineSystemMessageForSpeechTurnStrategy:
        return ConcreteDetermineSystemMessageForSpeechTurnStrategy(
            messages_to_llm, self._dialogue_initial_prompting_messages_provider_factory
        )
