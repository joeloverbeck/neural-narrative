from src.prompting.abstracts.abstract_factories import ToolResponseDataExtractionFactory
from src.prompting.abstracts.factory_products import ExtractedDataProduct
from src.prompting.products.concrete_extracted_data_product import ConcreteExtractedDataProduct


class SpeechToolResponseDataExtractionFactory(ToolResponseDataExtractionFactory):
    def __init__(self, parsed_tool_response: dict):
        assert parsed_tool_response

        self._parsed_tool_response = parsed_tool_response

    def extract_data(self) -> ExtractedDataProduct:
        # Extract the "arguments" dictionary from the tool response
        arguments = self._parsed_tool_response.get("arguments", {})

        return ConcreteExtractedDataProduct({
            "name": arguments.get("name"),
            "speech": arguments.get("speech"),
            "narration_text": arguments.get("narration_text")
        })
