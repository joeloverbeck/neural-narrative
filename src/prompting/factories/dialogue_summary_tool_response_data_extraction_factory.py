from src.prompting.abstracts.abstract_factories import ToolResponseDataExtractionProvider
from src.prompting.abstracts.factory_products import ExtractedDataProduct
from src.prompting.products.concrete_extracted_data_product import ConcreteExtractedDataProduct


class DialogueSummaryToolResponseDataExtractionFactory(ToolResponseDataExtractionProvider):

    def __init__(self, parsed_tool_response: dict):
        self._parsed_tool_response = parsed_tool_response

    def extract_data(self) -> ExtractedDataProduct:
        # Extract the "arguments" dictionary from the tool response
        return ConcreteExtractedDataProduct(self._parsed_tool_response.get("arguments", {}).get("summary"))
