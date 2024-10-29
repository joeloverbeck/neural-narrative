from typing import Protocol

from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct
from src.prompting.llm import Llm


class LlmClient(Protocol):

    def generate_completion(
        self, model: Llm, messages_to_llm: MessagesToLlm
    ) -> AiCompletionProduct:
        pass

    def generate_image(self, prompt: str) -> str:
        pass
