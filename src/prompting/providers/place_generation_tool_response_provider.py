import logging
from pathlib import Path
from typing import Optional, Dict

from pydantic import BaseModel

from src.base.constants import (
    PARENT_TEMPLATE_TYPE,
)
from src.base.enums import TemplateType
from src.base.products.dict_product import DictProduct
from src.base.validators import validate_non_empty_string
from src.filesystem.path_manager import PathManager
from src.maps.models.area import Area
from src.maps.models.location import get_custom_location_class
from src.maps.models.region import Region
from src.maps.models.room import get_custom_room_class
from src.maps.models.world import World
from src.maps.template_type_data import TemplateTypeData
from src.maps.templates_repository import TemplatesRepository
from src.prompting.abstracts.abstract_factories import (
    ToolResponseProvider,
    ProduceToolResponseStrategyFactory,
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
        templates_repository: Optional[TemplatesRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(father_place_identifier, "father_place_identifier")

        self._father_place_identifier = father_place_identifier
        self._template_type = template_type
        self._notion = notion

        self._templates_repository = templates_repository or TemplatesRepository()

    def _get_template_type_data(self) -> Optional[TemplateTypeData]:
        data_mapping: Dict[TemplateType, TemplateTypeData] = {
            TemplateType.WORLD: TemplateTypeData(
                prompt_file=self._path_manager.get_world_generation_prompt_path(),
                response_model=World,
            ),
            TemplateType.REGION: TemplateTypeData(
                prompt_file=self._path_manager.get_region_generation_prompt_path(),
                response_model=Region,
            ),
            TemplateType.AREA: TemplateTypeData(
                prompt_file=self._path_manager.get_area_generation_prompt_path(),
                response_model=Area,
            ),
            TemplateType.LOCATION: TemplateTypeData(
                prompt_file=self._path_manager.get_location_generation_prompt_path(),
                response_model=get_custom_location_class(),
            ),
            TemplateType.ROOM: TemplateTypeData(
                prompt_file=self._path_manager.get_room_generation_prompt_path(),
                response_model=get_custom_room_class(),
            ),
        }

        return data_mapping.get(self._template_type)

    def get_prompt_file(self) -> Path:
        template_data = self._get_template_type_data()
        if not template_data:
            raise ValueError(
                f"Failed to produce template data for father place identifier '{self._father_place_identifier}' and template type {self._template_type}."
            )
        return template_data.prompt_file

    def get_prompt_kwargs(self) -> dict:
        parent_templates_file = self._templates_repository.load_templates(
            PARENT_TEMPLATE_TYPE.get(self._template_type)
        )

        place_template = parent_templates_file[self._father_place_identifier]

        current_place_type_templates = self._templates_repository.load_templates(
            self._template_type
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

        # Both locations and rooms have types.
        if (
            self._template_type == TemplateType.LOCATION
            or self._template_type == TemplateType.ROOM
        ):
            arguments.update({"type": response_model.type})

        return DictProduct(arguments, is_valid=True)
