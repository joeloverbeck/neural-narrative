from typing import List

from openai import OpenAI

from src.constants import MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL
from src.dialogues.abstracts.abstract_factories import SpeechDataFactory
from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.factories.concrete_ai_completion_factory import ConcreteAiCompletionFactory
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.prompting.factories.speech_tool_response_data_extraction_factory import SpeechToolResponseDataExtractionFactory


class LlmSpeechDataFactory(SpeechDataFactory):

    def __init__(self, client: OpenAI, model: str, previous_messages: List[dict]):
        assert client
        assert model

        self._client = client
        self._model = model
        self._previous_messages = previous_messages
        self._max_retries = MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL

    def create_speech_data(self) -> SpeechDataProduct:

        while self._max_retries > 0:
            llm_content_product = OpenAiLlmContentFactory(client=self._client, model=self._model,
                                                          messages=self._previous_messages,
                                                          ai_completion_factory=ConcreteAiCompletionFactory(
                                                              self._client)).generate_content()

            if llm_content_product.is_valid():
                tool_response_parsing_product = ConcreteToolResponseParsingFactory(
                    llm_content_product.get()).parse_tool_response()

                if not tool_response_parsing_product.is_valid():
                    self._max_retries -= 1
                    print(
                        f"Was unable to parse the tool response: {tool_response_parsing_product.get()}. Error: {tool_response_parsing_product.get_error()}\nLLM response content: {llm_content_product.get()}")
                    continue

                self._previous_messages.append({"role": "assistant", "content": llm_content_product.get()})

                return ConcreteSpeechDataProduct(SpeechToolResponseDataExtractionFactory(
                    tool_response_parsing_product.get()).extract_data().get(), is_valid=True)

            # from this point on, the responses are invalid.
            self._max_retries -= 1
            print(f"LLM failed to produce a response: {llm_content_product.get_error()}")

        return ConcreteSpeechDataProduct({}, is_valid=False,
                                         error=f"Exhausted all retries when trying to get a valid response out of the LLM.")
