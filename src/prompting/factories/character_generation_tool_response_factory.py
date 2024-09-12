from src.constants import CHARACTER_GENERATOR_TOOL_FILE, CHARACTER_GENERATION_INSTRUCTIONS_FILE, \
    TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct
from src.tools import generate_tool_prompt


class CharacterGenerationToolResponseFactory(ToolResponseFactory):
    """
    Concrete Factories produce a family of products that belong to a single
    variant. The factory guarantees that resulting products are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    product, while inside the method a concrete product is instantiated.
    """

    def __init__(self, playthrough_name: str, user_input_on_character: str,
                 produce_tool_response_strategy: ProduceToolResponseStrategy):
        assert playthrough_name
        assert produce_tool_response_strategy

        self._playthrough_name = playthrough_name
        self._user_input_on_character = user_input_on_character
        self._produce_tool_response_strategy = produce_tool_response_strategy

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

        return ConcreteLlmToolResponseProduct(self._produce_tool_response_strategy.produce_tool_response(system_content,
                                                                                                         f"Create the bio for a character based in the world of {playthrough_metadata["world_template"]}. {self._user_input_on_character}"),
                                              is_valid=True)
