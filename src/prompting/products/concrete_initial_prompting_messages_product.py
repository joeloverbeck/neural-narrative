from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.dialogues.messages_to_llm import MessagesToLlm


class ConcreteInitialPromptingMessagesProduct(InitialPromptingMessagesProduct):

    def __init__(self, initial_prompting_messages: MessagesToLlm):
        self._initial_prompting_messages = initial_prompting_messages

    def get(self) -> MessagesToLlm:
        return self._initial_prompting_messages
