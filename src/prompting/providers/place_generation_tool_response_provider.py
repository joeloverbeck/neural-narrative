from typing import Optional, Dict

from src.base.constants import (
    AREA_GENERATION_PROMPT_FILE,
    REGION_GENERATION_PROMPT_FILE,
    LOCATION_GENERATION_PROMPT_FILE,
    REGION_GENERATION_TOOL_FILE,
    AREA_GENERATION_TOOL_FILE,
    LOCATION_GENERATION_TOOL_FILE,
    WORLDS_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    LOCATION_TYPES,
    WORLD_GENERATION_PROMPT_FILE,
    STORY_UNIVERSES_TEMPLATE_FILE,
    WORLD_GENERATION_TOOL_FILE,
)
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.template_type_data import TemplateTypeData
from src.prompting.abstracts.abstract_factories import (
    ToolResponseProvider,
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
        father_place_identifier: str,
        template_type: TemplateType,
        notion: str,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        validate_non_empty_string(father_place_identifier, "father_place_identifier")

        self._father_place_identifier = father_place_identifier
        self._template_type = template_type
        self._notion = notion

    def _get_tool_data(self) -> dict:
        tool_file = self.get_tool_file()

        if tool_file == LOCATION_GENERATION_TOOL_FILE:
            template_copy = self._filesystem_manager.load_existing_or_new_json_file(
                LOCATION_GENERATION_TOOL_FILE
            )
            try:
                template_copy["function"]["parameters"]["properties"]["type"][
                    "enum"
                ] = LOCATION_TYPES
            except Exception as e:
                raise ValueError(
                    f"Was unable to format the location generation tool file: {e}"
                )
            return template_copy
        return self._filesystem_manager.read_json_file(tool_file)

    def _get_template_type_data(self) -> Optional[TemplateTypeData]:
        data_mapping: Dict[TemplateType, TemplateTypeData] = {
            TemplateType.WORLD: TemplateTypeData(
                prompt_file=WORLD_GENERATION_PROMPT_FILE,
                father_templates_file_path=STORY_UNIVERSES_TEMPLATE_FILE,
                current_place_templates_file_path=WORLDS_TEMPLATES_FILE,
                tool_file=WORLD_GENERATION_TOOL_FILE,
            ),
            TemplateType.REGION: TemplateTypeData(
                prompt_file=REGION_GENERATION_PROMPT_FILE,
                father_templates_file_path=WORLDS_TEMPLATES_FILE,
                current_place_templates_file_path=REGIONS_TEMPLATES_FILE,
                tool_file=REGION_GENERATION_TOOL_FILE,
            ),
            TemplateType.AREA: TemplateTypeData(
                prompt_file=AREA_GENERATION_PROMPT_FILE,
                father_templates_file_path=REGIONS_TEMPLATES_FILE,
                current_place_templates_file_path=AREAS_TEMPLATES_FILE,
                tool_file=AREA_GENERATION_TOOL_FILE,
            ),
            TemplateType.LOCATION: TemplateTypeData(
                prompt_file=LOCATION_GENERATION_PROMPT_FILE,
                father_templates_file_path=AREAS_TEMPLATES_FILE,
                current_place_templates_file_path=LOCATIONS_TEMPLATES_FILE,
                tool_file=LOCATION_GENERATION_TOOL_FILE,
            ),
        }
        return data_mapping.get(self._template_type)

    def get_prompt_file(self) -> str:
        template_data = self._get_template_type_data()
        if not template_data:
            raise ValueError(
                f"Failed to produce template data for father place identifier '{self._father_place_identifier}' and template type {self._template_type}."
            )
        return template_data.prompt_file

    def get_prompt_kwargs(self) -> dict:
        template_data = self._get_template_type_data()
        father_templates_file = self._filesystem_manager.load_existing_or_new_json_file(
            template_data.father_templates_file_path
        )
        place_template = father_templates_file[self._father_place_identifier]
        current_place_type_templates = (
            self._filesystem_manager.load_existing_or_new_json_file(
                template_data.current_place_templates_file_path
            )
        )
        return {
            "father_place_name": self._father_place_identifier,
            "father_place_description": place_template["description"],
            "father_place_categories": place_template["categories"],
            "current_place_type_names": list(current_place_type_templates.keys()),
        }

    def get_tool_file(self) -> str:
        template_data = self._get_template_type_data()
        return template_data.tool_file

    def get_user_content(self) -> str:
        user_content = f"Create the name and description of a {self._template_type.value}, following the above instructions."
        if self._notion:
            user_content += (
                f" User guidance about how he wants this place to be: {self._notion}"
            )
        return user_content

    def create_product_from_dict(self, arguments: dict):
        return ConcreteLlmToolResponseProduct(arguments, is_valid=True)
