from typing import List

from openai import OpenAI

from src.constants import MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
from src.dialogues.abstracts.abstract_factories import SpeechDataFactory
from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import ProcessLlmContentIntoSpeechDataStrategy
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.factories.concrete_ai_completion_factory import ConcreteAiCompletionFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory


class LlmSpeechDataFactory(SpeechDataFactory):

    def __init__(self, client: OpenAI, model: str, previous_messages: List[dict],
                 process_llm_content_into_speech_data_strategy: ProcessLlmContentIntoSpeechDataStrategy):
        assert client
        assert model
        assert process_llm_content_into_speech_data_strategy

        self._client = client
        self._model = model
        self._previous_messages = previous_messages
        self._process_llm_content_into_speech_data_strategy = process_llm_content_into_speech_data_strategy

        self._max_retries = MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL

    def create_speech_data(self) -> SpeechDataProduct:
        while self._max_retries > 0:
            llm_content_product = OpenAiLlmContentFactory(client=self._client, model=self._model,
                                                          messages=self._previous_messages,
                                                          ai_completion_factory=ConcreteAiCompletionFactory(
                                                              self._client)).generate_content()

            speech_data_product = self._process_llm_content_into_speech_data_strategy.do_algorithm(llm_content_product)

            if speech_data_product.is_valid():
                return speech_data_product

            # from this point on, the responses are invalid.
            self._max_retries -= 1
            print(f"Failed to produce valid speech data: {speech_data_product.get_error()}")

        return ConcreteSpeechDataProduct({}, is_valid=False,
                                         error=f"Exhausted all retries when trying to get a valid response out of the LLM.")
