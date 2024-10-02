from typing import Optional, Dict

from src.constants import (
    AREA_GENERATION_PROMPT_FILE,
    REGION_GENERATION_PROMPT_FILE,
    LOCATION_GENERATION_PROMPT_FILE,
    REGION_GENERATION_TOOL_FILE,
    AREA_GENERATION_TOOL_FILE,
    LOCATION_GENERATION_TOOL_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.template_type_data import TemplateTypeData
from src.prompting.abstracts.abstract_factories import ToolResponseProvider
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class PlaceGenerationToolResponseProvider(
    BaseToolResponseProvider, ToolResponseProvider
):
    def __init__(
        self,
        place_identifier: str,
        template_type: TemplateType,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._place_identifier = place_identifier
        self._template_type = template_type

    def _get_template_type_data(self) -> Optional[TemplateTypeData]:
        data_mapping: Dict[TemplateType, TemplateTypeData] = {
            TemplateType.REGION: TemplateTypeData(
                prompt_file=REGION_GENERATION_PROMPT_FILE,
                father_templates_file_path=self._filesystem_manager.get_file_path_to_worlds_template_file(),
                current_place_templates_file_path=self._filesystem_manager.get_file_path_to_regions_template_file(),
                tool_file=REGION_GENERATION_TOOL_FILE,
            ),
            TemplateType.AREA: TemplateTypeData(
                prompt_file=AREA_GENERATION_PROMPT_FILE,
                father_templates_file_path=self._filesystem_manager.get_file_path_to_regions_template_file(),
                current_place_templates_file_path=self._filesystem_manager.get_file_path_to_areas_template_file(),
                tool_file=AREA_GENERATION_TOOL_FILE,
            ),
            TemplateType.LOCATION: TemplateTypeData(
                prompt_file=LOCATION_GENERATION_PROMPT_FILE,
                father_templates_file_path=self._filesystem_manager.get_file_path_to_areas_template_file(),
                current_place_templates_file_path=self._filesystem_manager.get_file_path_to_locations_template_file(),
                tool_file=LOCATION_GENERATION_TOOL_FILE,
            ),
        }
        return data_mapping.get(self._template_type)

    def create_llm_response(self) -> LlmToolResponseProduct:
        template_data = self._get_template_type_data()
        if not template_data:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Unknown template type '{self._template_type}'.",
            )

        # Load and format the corresponding prompt
        place_generation_prompt = self._read_prompt_file(template_data.prompt_file)

        # Load the father templates file
        father_templates_file = self._filesystem_manager.load_existing_or_new_json_file(
            template_data.father_templates_file_path
        )

        # Get the place template
        if self._place_identifier not in father_templates_file:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Place identifier '{self._place_identifier}' not found in father templates.",
            )
        place_template = father_templates_file[self._place_identifier]

        # Load current place type templates
        current_place_type_templates = (
            self._filesystem_manager.load_existing_or_new_json_file(
                template_data.current_place_templates_file_path
            )
        )

        # Format the prompt
        place_generation_prompt = self._format_prompt(
            place_generation_prompt,
            father_place_name=self._place_identifier,
            father_place_description=place_template["description"],
            father_place_categories=place_template["categories"],
            current_place_type_names=list(current_place_type_templates.keys()),
        )

        # Generate the tool prompt
        tool_data = self._read_tool_file(template_data.tool_file)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = self._generate_system_content(
            place_generation_prompt, tool_prompt
        )

        # Generate the response
        user_guidance = input(
            "Do you have any notion of how you want this place to be? (can be left empty): "
        )

        user_content = f"Create the name and description of a {self._template_type.value}, following the above instructions."

        if user_guidance:
            user_content += (
                f" User guidance about how he wants this place to be: {user_guidance}"
            )

        # Produce tool response
        tool_response = self._produce_tool_response(system_content, user_content)

        return ConcreteLlmToolResponseProduct(tool_response, is_valid=True)
