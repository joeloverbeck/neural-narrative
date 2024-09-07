from src.constants import HERMES_405B, CHARACTER_GENERATOR_TOOL_FILE, CHARACTER_GENERATION_INSTRUCTIONS_FILE, \
    TOOL_INSTRUCTIONS_FILE
from src.files import read_json_file, read_file
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct
from src.tools import generate_tool_prompt


class CharacterGenerationToolResponseFactory(ToolResponseFactory):
    """
    Concrete Factories produce a family of products that belong to a single
    variant. The factory guarantees that resulting products are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    product, while inside the method a concrete product is instantiated.
    """

    def __init__(self, client, user_input_on_character: str):
        self._client = client
        self._user_input_on_character = user_input_on_character

    def create_llm_response(self) -> LlmToolResponseProduct:
        system_content = read_file(CHARACTER_GENERATION_INSTRUCTIONS_FILE) + "\n\n" + generate_tool_prompt(
            read_json_file(CHARACTER_GENERATOR_TOOL_FILE), read_file(TOOL_INSTRUCTIONS_FILE))

        llm_content_product = OpenAiLlmContentFactory(self._client, HERMES_405B, [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": f"Create the bio for a character based in the post-apocalypse. {self._user_input_on_character}",
            },
        ]).generate_content()

        if not llm_content_product.is_valid():
            raise ValueError(f"Failed to receive content from LLM: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the response from the LLM, intending to get a tool call: {tool_response_parsing_product.get_error()}")

        return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=True)
