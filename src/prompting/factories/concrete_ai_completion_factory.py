from json import JSONDecodeError
from typing import List

from openai import OpenAI

from src.prompting.abstracts.abstract_factories import AiCompletionFactory
from src.prompting.abstracts.factory_products import AiCompletionProduct
from src.prompting.products.concrete_ai_completion_product import ConcreteAiCompletionProduct


class ConcreteAiCompletionFactory(AiCompletionFactory):
    def __init__(self, client: OpenAI):
        assert client
        self._client = client

    def generate_completion(self, model: str, messages: List[dict], temperature=1.0, top_p=1.0) -> AiCompletionProduct:
        # Surprisingly, this could fail. I got a JSONDecodeError

        try:
            completion = self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p
            )
            return ConcreteAiCompletionProduct(completion)
        except JSONDecodeError as error:
            return ConcreteAiCompletionProduct(None)
