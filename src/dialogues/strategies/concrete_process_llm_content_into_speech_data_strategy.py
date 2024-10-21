from src.base.required_string import RequiredString
from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import ProcessLlmContentIntoSpeechDataStrategy
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_speech_data_product import (
    ConcreteSpeechDataProduct,
)
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.factories.speech_tool_response_data_extraction_provider_factory import (
    SpeechToolResponseDataExtractionProviderFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)


class ConcreteProcessLlmContentIntoSpeechDataStrategy(
    ProcessLlmContentIntoSpeechDataStrategy
):
    def __init__(
        self,
        messages_to_llm: MessagesToLlm,
        tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
        speech_tool_response_data_extraction_provider_factory: SpeechToolResponseDataExtractionProviderFactory,
    ):
        self._messages_to_llm = messages_to_llm

        self._tool_response_parsing_provider_factory = (
            tool_response_parsing_provider_factory
        )
        self._speech_tool_response_data_extraction_provider_factory = (
            speech_tool_response_data_extraction_provider_factory
        )

    def do_algorithm(self, llm_content_product: LlmContentProduct) -> SpeechDataProduct:
        if not llm_content_product.is_valid():
            return ConcreteSpeechDataProduct(
                {}, is_valid=False, error=llm_content_product.get_error()
            )

        tool_response_parsing_product = self._tool_response_parsing_provider_factory.create_tool_response_parsing_provider(
            llm_content_product
        ).parse_tool_response()

        # Could be at this point that although the content is valid from an LLM perspective,
        # it still can't be parsed into a proper tool response.
        if not tool_response_parsing_product.is_valid():
            return ConcreteSpeechDataProduct(
                {},
                is_valid=False,
                error=f"Was unable to parse the tool response: {tool_response_parsing_product.get()}. Error: {tool_response_parsing_product.get_error()}\nLLM response content: {llm_content_product.get()}",
            )

        # At this point, the tool response has been parsed correctly, so it needs to be added
        # as the assistant's response.
        self._messages_to_llm.add_message(
            RequiredString("assistant"), llm_content_product.get()
        )

        speech_turn_response = self._speech_tool_response_data_extraction_provider_factory.create_speech_tool_response_data_extraction_provider(
            tool_response_parsing_product
        )

        return ConcreteSpeechDataProduct(
            speech_turn_response.extract_data().get(), is_valid=True
        )
