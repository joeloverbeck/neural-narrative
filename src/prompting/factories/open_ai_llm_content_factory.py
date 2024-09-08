from time import sleep
from typing import List

from openai import OpenAI

from src.constants import WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR, WAIT_TIME_WHEN_UNAUTHORIZED_ERROR, \
    WAIT_TIME_WHEN_EMPTY_CONTENT, MAX_RETRIES, \
    WAIT_TIME_WHEN_MALFORMED_COMPLETION
from src.enums import AiCompletionErrorType
from src.prompting.abstracts.abstract_factories import LlmContentFactory, AiCompletionFactory
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.products.concrete_llm_content_product import ConcreteLlmContentProduct


class OpenAiLlmContentFactory(LlmContentFactory):
    def __init__(self, client: OpenAI, model: str, messages: List[dict], ai_completion_factory: AiCompletionFactory,
                 max_retries=MAX_RETRIES,
                 temperature=1.0, top_p=1.0):
        assert messages
        assert len(messages) >= 1
        assert ai_completion_factory

        self._client = client
        self._model = model
        self._messages = messages
        self._ai_completion_factory = ai_completion_factory
        self._max_retries = max_retries
        self._temperature = temperature
        self._top_p = top_p
        self._retry_count = 0

    def generate_content(self) -> LlmContentProduct:
        while self._retry_count < self._max_retries:
            ai_completion_product = self._ai_completion_factory.generate_completion(
                model=self._model,
                messages=self._messages,
                temperature=self._temperature,
                top_p=self._top_p
            )

            if ai_completion_product.is_valid():
                self._retry_count = 0  # Reset retry count if we get a valid response
                return ConcreteLlmContentProduct(ai_completion_product.get(), is_valid=True)

            self._retry_count += 1

            if ai_completion_product.get_error() == AiCompletionErrorType.TOO_MANY_REQUESTS:
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to too many requests. Retrying in {WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR}...")
                sleep(WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR)
            elif ai_completion_product.get_error() == AiCompletionErrorType.UNAUTHORIZED:
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to unauthorized access. Retrying in {WAIT_TIME_WHEN_UNAUTHORIZED_ERROR}...")
                sleep(WAIT_TIME_WHEN_UNAUTHORIZED_ERROR)
            elif ai_completion_product.get_error() == AiCompletionErrorType.MALFORMED_COMPLETION:
                print(f"The completion returned by the AI was malformed.")
                sleep(WAIT_TIME_WHEN_MALFORMED_COMPLETION)
            elif ai_completion_product.get_error() == AiCompletionErrorType.EMPTY_CONTENT:
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to empty content returned by LLM. Retrying in {WAIT_TIME_WHEN_EMPTY_CONTENT}...")
                sleep(WAIT_TIME_WHEN_EMPTY_CONTENT)
            else:
                print(f"Attempt {self._retry_count}/{self._max_retries} failed due to an unhandled reason. Retrying...")

        return ConcreteLlmContentProduct(content="", is_valid=False, error="Max retries reached. No valid response.")
