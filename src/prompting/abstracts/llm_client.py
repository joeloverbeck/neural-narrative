from typing import Protocol
from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct


class LlmClient(Protocol):

    def generate_completion(self, model: str, messages_to_llm:
    MessagesToLlm, temperature=1.0, top_p=1.0) -> AiCompletionProduct:
        pass

    def generate_image(self, prompt: str) -> str:
        pass
