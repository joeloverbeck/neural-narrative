from typing import Optional, Dict

from src.constants import (
    AREA_GENERATION_PROMPT_FILE,
    REGION_GENERATION_PROMPT_FILE,
    LOCATION_GENERATION_PROMPT_FILE,
    REGION_GENERATION_TOOL_FILE,
    AREA_GENERATION_TOOL_FILE,
    LOCATION_GENERATION_TOOL_FILE,
    WORLD_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    LOCATION_TYPES,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.template_type_data import TemplateTypeData
from src.prompting.abstracts.abstract_factories import ToolResponseProvider
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
        notion: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._place_identifier = place_identifier
        self._template_type = template_type
        self._notion = notion

    def _read_and_format_tool_file(self, tool_file: str) -> dict:
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

    def _read_tool_file(self, tool_file: str) -> dict:
        return self._read_and_format_tool_file(tool_file)

    def _get_template_type_data(self) -> Optional[TemplateTypeData]:
        data_mapping: Dict[TemplateType, TemplateTypeData] = {
            TemplateType.REGION: TemplateTypeData(
                prompt_file=REGION_GENERATION_PROMPT_FILE,
                father_templates_file_path=WORLD_TEMPLATES_FILE,
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

        return template_data.prompt_file

    def get_prompt_kwargs(self) -> dict:
        template_data = self._get_template_type_data()
        father_templates_file = self._filesystem_manager.load_existing_or_new_json_file(
            template_data.father_templates_file_path
        )
        place_template = father_templates_file[self._place_identifier]
        current_place_type_templates = (
            self._filesystem_manager.load_existing_or_new_json_file(
                template_data.current_place_templates_file_path
            )
        )

        return {
            "father_place_name": self._place_identifier,
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

    def create_product(self, arguments: dict):
        return ConcreteLlmToolResponseProduct(arguments, is_valid=True)
