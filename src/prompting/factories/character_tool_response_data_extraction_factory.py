from src.prompting.abstracts.abstract_factories import ToolResponseDataExtractionFactory
from src.prompting.abstracts.factory_products import ExtractedDataProduct
from src.prompting.products.concrete_extracted_data_product import ConcreteExtractedDataProduct


class CharacterToolResponseDataExtractionFactory(ToolResponseDataExtractionFactory):

    def __init__(self, parsed_tool_response: dict):
        assert parsed_tool_response

        self._parsed_tool_response = parsed_tool_response

    def extract_data(self) -> ExtractedDataProduct:
        # Extract the "arguments" dictionary from the tool response
        arguments = self._parsed_tool_response.get("arguments", {})

        # Build the result JSON from the extracted fields
        return ConcreteExtractedDataProduct({
            "name": arguments.get("name"),
            "description": arguments.get("description"),
            "personality": arguments.get("personality"),
            "profile": arguments.get("profile"),
            "likes": arguments.get("likes"),
            "dislikes": arguments.get("dislikes"),
            "first message": arguments.get("first message"),
            "speech patterns": arguments.get("speech patterns"),
            "equipment": arguments.get("equipment")
        })
