from src.constants import CHARACTER_GENERATOR_TOOL_FILE, CHARACTER_GENERATION_INSTRUCTIONS_FILE, \
    TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.places_parameter import PlacesParameter
from src.prompting.abstracts.abstract_factories import ToolResponseFactory
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct
from src.tools import generate_tool_prompt


class CharacterGenerationToolResponseFactory(ToolResponseFactory):

    def __init__(self, playthrough_name: str, places_parameter: PlacesParameter,
                 produce_tool_response_strategy: ProduceToolResponseStrategy):
        assert playthrough_name
        assert places_parameter
        assert produce_tool_response_strategy

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._produce_tool_response_strategy = produce_tool_response_strategy

    def create_llm_response(self) -> LlmToolResponseProduct:
        filesystem_manager = FilesystemManager()

        character_generation_instructions = filesystem_manager.read_file(
            CHARACTER_GENERATION_INSTRUCTIONS_FILE)

        playthrough_metadata = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        worlds_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        # Now also load the templates of regions, areas, and locations.
        regions_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_regions_template_file())

        areas_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_areas_template_file())

        locations_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_locations_template_file())

        location_name = ""
        location_description = ""

        if self._places_parameter.get_location_template():
            location_name = f"Here's the description of the location {self._places_parameter.get_location_template()}:\n"
            location_description = f"{locations_template[self._places_parameter.get_location_template()]["description"]}"

        character_generation_instructions = character_generation_instructions.format(
            world_name=playthrough_metadata["world_template"],
            world_description=
            worlds_template[playthrough_metadata["world_template"]][
                "description"],
            region_name=self._places_parameter.get_region_template(),
            region_description=regions_template[self._places_parameter.get_region_template()]["description"],
            area_name=self._places_parameter.get_area_template(),
            area_description=areas_template[self._places_parameter.get_area_template()]["description"],
            location_name=location_name,
            location_description=location_description)

        system_content = character_generation_instructions + "\n\n" + generate_tool_prompt(
            filesystem_manager.read_json_file(CHARACTER_GENERATOR_TOOL_FILE),
            filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE))

        return ConcreteLlmToolResponseProduct(self._produce_tool_response_strategy.produce_tool_response(system_content,
                                                                                                         f"Create the bio for a character influenced by the places described above."),
                                              is_valid=True)
