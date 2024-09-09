from typing import List

from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import ProcessLlmContentIntoSpeechDataStrategy
from src.dialogues.products.concrete_speech_data_product import ConcreteSpeechDataProduct
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.speech_tool_response_data_extraction_factory import SpeechToolResponseDataExtractionFactory


class ConcreteProcessLlmContentIntoSpeechDataStrategy(ProcessLlmContentIntoSpeechDataStrategy):
    def __init__(self, previous_messages: List[dict]):
        self._previous_messages = previous_messages

    def do_algorithm(self, llm_content_product: LlmContentProduct) -> SpeechDataProduct:
        if not llm_content_product.is_valid():
            return ConcreteSpeechDataProduct({}, is_valid=False, error=llm_content_product.get_error())

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        # Could be at this point that although the content is valid from an LLM perspective,
        # it still can't be parsed into a proper tool response.
        if not tool_response_parsing_product.is_valid():
            return ConcreteSpeechDataProduct({}, is_valid=False,
                                             error=f"Was unable to parse the tool response: {tool_response_parsing_product.get()}. Error: {tool_response_parsing_product.get_error()}\nLLM response content: {llm_content_product.get()}")

        # At this point, the tool response has been parsed correctly, so it needs to be added
        # as the assistant's response.
        self._previous_messages.append({"role": "assistant", "content": llm_content_product.get()})

        return ConcreteSpeechDataProduct(SpeechToolResponseDataExtractionFactory(
            tool_response_parsing_product.get()).extract_data().get(), is_valid=True)
