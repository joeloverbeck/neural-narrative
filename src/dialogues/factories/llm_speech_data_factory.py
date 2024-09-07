from typing import List

from src.constants import HERMES_405B
from src.dialogues.abstracts.abstract_factories import SpeechDataFactory
from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.prompting.factories.speech_tool_response_data_extraction_factory import SpeechToolResponseDataExtractionFactory


class LlmSpeechDataFactory(SpeechDataFactory):

    def __init__(self, client, previous_messages: List[dict]):
        assert client

        self._client = client
        self._previous_messages = previous_messages

    def create_speech_data(self) -> SpeechDataProduct:

        llm_content_product = OpenAiLlmContentFactory(client=self._client, model=HERMES_405B,
                                                      messages=self._previous_messages).generate_content()
        if not llm_content_product.is_valid():
            return ConcreteSpeechDataProduct({}, is_valid=False,
                                             error=f"LLM failed to produce a response: {llm_content_product.get_error()}")

        self._previous_messages.append({"role": "assistant", "content": llm_content_product.get()})

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Was unable to parse the tool response: {tool_response_parsing_product.get()}\nLLM response content: {llm_content_product.get()}")

        return ConcreteSpeechDataProduct(SpeechToolResponseDataExtractionFactory(
            tool_response_parsing_product.get()).extract_data().get(), is_valid=True)
