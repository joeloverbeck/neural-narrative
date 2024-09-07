from typing import List

from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct


class ConcreteInitialPromptingMessagesProduct(InitialPromptingMessagesProduct):
    def __init__(self, initial_prompting_messages: List[dict]):
        self._initial_prompting_messages = initial_prompting_messages

    def get(self) -> List[dict]:
        return self._initial_prompting_messages
