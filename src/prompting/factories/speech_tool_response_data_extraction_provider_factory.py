from src.prompting.abstracts.factory_products import ToolResponseParsingProduct
from src.prompting.providers.speech_tool_response_data_extraction_provider import \
    SpeechToolResponseDataExtractionProvider


class SpeechToolResponseDataExtractionProviderFactory:
    @staticmethod
    def create_speech_tool_response_data_extraction_provider(
            tool_response_parsing_product: ToolResponseParsingProduct) -> SpeechToolResponseDataExtractionProvider:
        return SpeechToolResponseDataExtractionProvider(
            tool_response_parsing_product.get())
