from openai import OpenAI

from src.constants import CHARACTER_GENERATOR_TOOL_FILE, CHARACTER_GENERATION_INSTRUCTIONS_FILE, \
    TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.concrete_ai_completion_factory import ConcreteAiCompletionFactory
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

    def __init__(self, playthrough_name: str, client: OpenAI, model: str, user_input_on_character: str):
        assert playthrough_name
        assert client
        assert model

        self._playthrough_name = playthrough_name
        self._client = client
        self._model = model
        self._user_input_on_character = user_input_on_character

    def create_llm_response(self) -> LlmToolResponseProduct:
        filesystem_manager = FilesystemManager()

        character_generation_instructions = filesystem_manager.read_file(
            CHARACTER_GENERATION_INSTRUCTIONS_FILE)

        playthrough_metadata = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        worlds_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        character_generation_instructions = character_generation_instructions.format(
            world_name=playthrough_metadata["world_template"],
            world_description=
            worlds_template[playthrough_metadata["world_template"]][
                "description"])

        system_content = character_generation_instructions + "\n\n" + generate_tool_prompt(
            filesystem_manager.read_json_file(CHARACTER_GENERATOR_TOOL_FILE),
            filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE))

        print(system_content)

        llm_content_product = OpenAiLlmContentFactory(self._client, self._model, [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": f"Create the bio for a character based in the world of {playthrough_metadata["world_template"]}. {self._user_input_on_character}",
            },
        ], ConcreteAiCompletionFactory(self._client)).generate_content()

        if not llm_content_product.is_valid():
            raise ValueError(f"Failed to receive content from LLM: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the response from the LLM, intending to get a tool call: {tool_response_parsing_product.get_error()}")

        return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=True)
