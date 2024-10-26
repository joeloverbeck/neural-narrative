import logging
from pathlib import Path
from typing import Optional, Dict

from pydantic import BaseModel

from src.base.constants import (
    AREA_GENERATION_PROMPT_FILE,
    REGION_GENERATION_PROMPT_FILE,
    LOCATION_GENERATION_PROMPT_FILE,
    WORLDS_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    WORLD_GENERATION_PROMPT_FILE,
    STORY_UNIVERSES_TEMPLATE_FILE,
)
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.models.area import Area
from src.maps.models.location import get_custom_location_class
from src.maps.models.region import Region
from src.maps.models.world import World
from src.maps.template_type_data import TemplateTypeData
from src.prompting.abstracts.abstract_factories import (
    ToolResponseProvider,
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


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

    def _get_template_type_data(self) -> Optional[TemplateTypeData]:
        data_mapping: Dict[TemplateType, TemplateTypeData] = {
            TemplateType.WORLD: TemplateTypeData(
                prompt_file=WORLD_GENERATION_PROMPT_FILE,
                father_templates_file_path=STORY_UNIVERSES_TEMPLATE_FILE,
                current_place_templates_file_path=WORLDS_TEMPLATES_FILE,
                response_model=World,
            ),
            TemplateType.REGION: TemplateTypeData(
                prompt_file=REGION_GENERATION_PROMPT_FILE,
                father_templates_file_path=WORLDS_TEMPLATES_FILE,
                current_place_templates_file_path=REGIONS_TEMPLATES_FILE,
                response_model=Region,
            ),
            TemplateType.AREA: TemplateTypeData(
                prompt_file=AREA_GENERATION_PROMPT_FILE,
                father_templates_file_path=REGIONS_TEMPLATES_FILE,
                current_place_templates_file_path=AREAS_TEMPLATES_FILE,
                response_model=Area,
            ),
            TemplateType.LOCATION: TemplateTypeData(
                prompt_file=LOCATION_GENERATION_PROMPT_FILE,
                father_templates_file_path=AREAS_TEMPLATES_FILE,
                current_place_templates_file_path=LOCATIONS_TEMPLATES_FILE,
                response_model=get_custom_location_class(),
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
        father_templates_file = read_json_file(
            Path(template_data.father_templates_file_path)
        )
        place_template = father_templates_file[self._father_place_identifier]
        current_place_type_templates = read_json_file(
            Path(template_data.current_place_templates_file_path)
        )
        return {
            "father_place_name": self._father_place_identifier,
            "father_place_description": place_template["description"],
            "father_place_categories": place_template["categories"],
            "current_place_type_names": list(current_place_type_templates.keys()),
        }

    def get_user_content(self) -> str:
        user_content = f"Create the name and description of a {self._template_type.value}, following the above instructions."
        if self._notion:
            user_content += (
                f" User guidance about how he wants this place to be: {self._notion}"
            )
        return user_content

    def create_product_from_base_model(self, response_model: BaseModel):

        description = str(response_model.description)

        arguments = {
            "name": response_model.name,
            "description": description.replace("\n\n", "\n"),
        }

        if self._template_type == TemplateType.LOCATION:
            arguments.update({"type": response_model.type})

        return ConcreteLlmToolResponseProduct(arguments, is_valid=True)
