from src.prompting.abstracts.abstract_factories import (
    ToolResponseDataExtractionProvider,
)
from src.prompting.abstracts.factory_products import ExtractedDataProduct
from src.prompting.products.concrete_extracted_data_product import (
    ConcreteExtractedDataProduct,
)


class SpeechToolResponseDataExtractionProvider(ToolResponseDataExtractionProvider):

    def __init__(self, parsed_tool_response: dict):
        assert parsed_tool_response
        self._parsed_tool_response = parsed_tool_response

    def extract_data(self) -> ExtractedDataProduct:
        arguments = self._parsed_tool_response.get("arguments", {})
        return ConcreteExtractedDataProduct(
            {
                "name": arguments.get("name"),
                "speech": arguments.get("speech"),
                "narration_text": arguments.get("narration_text"),
            }
        )
