import logging
from json import JSONDecodeError

from openai import OpenAI

from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.products.concrete_ai_completion_product import (
    ConcreteAiCompletionProduct,
)

logger = logging.getLogger(__name__)


class OpenAiLlmClient(LlmClient):

    def __init__(self, client: OpenAI):
        if not client:
            raise ValueError("client must not be empty.")
        # Unless you supress logging messages lower than WARNING, the log file will get swamped with messages.
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self._client = client

    def generate_completion(
        self, model: str, messages_to_llm: MessagesToLlm, temperature=1.0, top_p=1.0
    ) -> AiCompletionProduct:
        try:
            completion = self._client.chat.completions.create(
                model=model,
                messages=messages_to_llm.get(),
                temperature=temperature,
                top_p=top_p,
            )
            return ConcreteAiCompletionProduct(completion)
        except JSONDecodeError as error:
            logger.error(f"Failed to decode JSON: %s.", error)
            return ConcreteAiCompletionProduct(None)

    def generate_image(self, prompt: str) -> str:
        response = self._client.images.generate(
            model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1
        )
        return response.data[0].url
