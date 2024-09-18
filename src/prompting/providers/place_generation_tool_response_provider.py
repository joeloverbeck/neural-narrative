from typing import Optional

from src.constants import (
    AREA_GENERATION_PROMPT_FILE,
    REGION_GENERATION_PROMPT_FILE,
    LOCATION_GENERATION_PROMPT_FILE,
    REGION_GENERATION_TOOL_FILE,
    TOOL_INSTRUCTIONS_FILE,
    AREA_GENERATION_TOOL_FILE,
    LOCATION_GENERATION_TOOL_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import ToolResponseProvider
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.tools import generate_tool_prompt


class PlaceGenerationToolResponseProvider(ToolResponseProvider):
    def __init__(
            self,
            place_identifier: str,
            template_type: TemplateType,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        assert place_identifier
        assert template_type

        self._place_identifier = place_identifier
        self._template_type = template_type
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_llm_response(self) -> LlmToolResponseProduct:
        # Must load and format the corresponding prompt
        filesystem_manager = FilesystemManager()

        place_generation_prompt: Optional[str]

        if self._template_type == TemplateType.REGION:
            place_generation_prompt = filesystem_manager.read_file(
                REGION_GENERATION_PROMPT_FILE
            )

        elif self._template_type == TemplateType.AREA:
            place_generation_prompt = filesystem_manager.read_file(
                AREA_GENERATION_PROMPT_FILE
            )

        elif self._template_type == TemplateType.LOCATION:
            place_generation_prompt = filesystem_manager.read_file(
                LOCATION_GENERATION_PROMPT_FILE
            )
        else:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Don't know how to load generation prompt for template '{self._template_type}'.",
            )

        # now load the corresponding father templates file
        father_templates_file: Optional[dict]

        if self._template_type == TemplateType.REGION:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_worlds_template_file()
            )

        elif self._template_type == TemplateType.AREA:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_regions_template_file()
            )

        elif self._template_type == TemplateType.LOCATION:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_areas_template_file()
            )
        else:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Don't know how to load the father templates file for template '{self._template_type}'.",
            )

        place_template = father_templates_file[self._place_identifier]

        current_place_type_templates: Optional[dict]

        if self._template_type == TemplateType.REGION:
            current_place_type_templates = (
                filesystem_manager.load_existing_or_new_json_file(
                    filesystem_manager.get_file_path_to_regions_template_file()
                )
            )
        elif self._template_type == TemplateType.AREA:
            current_place_type_templates = (
                filesystem_manager.load_existing_or_new_json_file(
                    filesystem_manager.get_file_path_to_areas_template_file()
                )
            )
        elif self._template_type == TemplateType.LOCATION:
            current_place_type_templates = (
                filesystem_manager.load_existing_or_new_json_file(
                    filesystem_manager.get_file_path_to_locations_template_file()
                )
            )
        else:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Don't know how to load the current place type templates for template '{self._template_type}'.",
            )

        # Now we have all the necessary information to format the prompt
        place_generation_prompt = place_generation_prompt.format(
            father_place_name=self._place_identifier,
            father_place_description=place_template["description"],
            father_place_categories=place_template["categories"],
            current_place_type_names=list(current_place_type_templates.keys()),
        )

        system_content = place_generation_prompt + "\n\n"

        if self._template_type == TemplateType.REGION:
            system_content += generate_tool_prompt(
                filesystem_manager.read_json_file(REGION_GENERATION_TOOL_FILE),
                filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            )
        elif self._template_type == TemplateType.AREA:
            system_content += generate_tool_prompt(
                filesystem_manager.read_json_file(AREA_GENERATION_TOOL_FILE),
                filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            )
        elif self._template_type == TemplateType.LOCATION:
            system_content += generate_tool_prompt(
                filesystem_manager.read_json_file(LOCATION_GENERATION_TOOL_FILE),
                filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            )
        else:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"Don't know how to create the tool part of the prompt for template '{self._template_type}'.",
            )

        return ConcreteLlmToolResponseProduct(
            self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy().produce_tool_response(
                system_content,
                f"Create the name and description of a {self._template_type.value}, following the above instructions.",
            ),
            is_valid=True,
        )
