from src.dialogues.abstracts.strategies import DetermineSystemMessageForSpeechTurnStrategy
from src.dialogues.factories.dialogue_initial_prompting_messages_provider_factory import \
    DialogueInitialPromptingMessagesProviderFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConcreteDetermineSystemMessageForSpeechTurnStrategy(
    DetermineSystemMessageForSpeechTurnStrategy):

    def __init__(self, messages_to_llm: MessagesToLlm,
                 dialogue_initial_prompting_messages_provider_factory:
                 DialogueInitialPromptingMessagesProviderFactory):
        if not messages_to_llm:
            raise ValueError("messages_to_llm can't be empty.")
        self._messages_to_llm = messages_to_llm
        self._dialogue_initial_prompting_messages_provider_factory = (
            dialogue_initial_prompting_messages_provider_factory)

    def do_algorithm(self, speech_turn_choice_tool_response_product:
    LlmToolResponseProduct):
        dialogue_initial_prompting_messages_product = (self.
                                                       _dialogue_initial_prompting_messages_provider_factory.
                                                       create_dialogue_initial_prompting_messages_provider(
            speech_turn_choice_tool_response_product).
                                                       create_initial_prompting_messages())
        self._messages_to_llm.extend_from_messages_to_llm(
            dialogue_initial_prompting_messages_product.get())
