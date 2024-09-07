from time import sleep
from typing import List

from src.constants import WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR, WAIT_TIME_WHEN_UNAUTHORIZED_ERROR, \
    TOO_MANY_REQUESTS_ERROR_NUMBER, UNAUTHORIZED_ERROR_NUMBER, WAIT_TIME_WHEN_EMPTY_CONTENT, MAX_RETRIES, \
    WAIT_TIME_WHEN_MALFORMED_COMPLETION
from src.prompting.abstracts.abstract_factories import LlmContentFactory
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.products.concrete_llm_content_product import ConcreteLlmContentProduct
from src.prompting.prompting import is_valid_response, does_response_contain_content


class OpenAiLlmContentFactory(LlmContentFactory):
    def __init__(self, client, model, messages: List[dict], max_retries=MAX_RETRIES, temperature=1.0, top_p=1.0):
        assert messages
        assert len(messages) >= 1

        self._client = client
        self._model = model
        self._messages = messages
        self._max_retries = max_retries
        self._temperature = temperature
        self._top_p = top_p
        self._retry_count = 0

    def generate_content(self) -> LlmContentProduct:
        while self._retry_count < self._max_retries:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=self._messages,
                temperature=self._temperature,
                top_p=self._top_p
            )

            if is_valid_response(completion):
                self._retry_count = 0  # Reset retry count if we get a valid response
                return ConcreteLlmContentProduct(completion.choices[0].message.content, is_valid=True)

            self._retry_count += 1

            if hasattr(completion, 'error') and completion.error['code'] == TOO_MANY_REQUESTS_ERROR_NUMBER:
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to too many requests. Retrying in {WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR}...")
                sleep(WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR)
            elif hasattr(completion, 'error') and completion.error['code'] == UNAUTHORIZED_ERROR_NUMBER:
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to unauthorized access. Retrying in {WAIT_TIME_WHEN_UNAUTHORIZED_ERROR}...")
                sleep(WAIT_TIME_WHEN_UNAUTHORIZED_ERROR)
            elif not completion.choices:
                print(f"Completion object didn't return 'choices': {completion}")
                sleep(WAIT_TIME_WHEN_MALFORMED_COMPLETION)
            elif not does_response_contain_content(completion):
                print(
                    f"Attempt {self._retry_count}/{self._max_retries} failed due to empty content returned by LLM. Retrying in {WAIT_TIME_WHEN_EMPTY_CONTENT}...")
                sleep(WAIT_TIME_WHEN_EMPTY_CONTENT)
            else:
                print(f"Attempt {self._retry_count}/{self._max_retries} failed due to an unhandled reason. Retrying...")
                print(completion)

        return ConcreteLlmContentProduct(content="", is_valid=False, error="Max retries reached. No valid response.")
