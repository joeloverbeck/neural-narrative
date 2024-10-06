import logging
from typing import Optional

from src.abstracts.command import Command
from src.config.config_manager import ConfigManager
from src.constants import (
    WORLD_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.abstracts.interface_manager import InterfaceManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)

logger = logging.getLogger(__name__)


class GeneratePlaceCommand(Command):
    def __init__(
        self,
        place_template_type: TemplateType,
        father_place_template_type: TemplateType,
        father_place_name: str,
        notion: str,
        interface_manager: InterfaceManager = None,
        filesystem_manager: FilesystemManager = None,
        config_manager: ConfigManager = None,
    ):
        if not father_place_name:
            raise ValueError("father_place_name can't be empty.")

        self._place_template_type = place_template_type
        self._father_place_template_type = father_place_template_type
        self._father_place_name = father_place_name
        self._notion = notion

        # sanity check
        if (
            self._place_template_type == TemplateType.REGION
            and self._father_place_template_type != TemplateType.WORLD
        ):
            raise ValueError(
                f"Attempted to create a region from something other than a world! The father place was '{self._father_place_template_type}'."
            )
        if (
            self._place_template_type == TemplateType.AREA
            and self._father_place_template_type != TemplateType.REGION
        ):
            raise ValueError(
                f"Attempted to create an area from something other than a region! The father place was '{self._father_place_template_type}'."
            )
        if (
            self._place_template_type == TemplateType.LOCATION
            and self._father_place_template_type != TemplateType.AREA
        ):
            raise ValueError(
                f"Attempted to create a location from something other than an area! The father place was '{self._father_place_template_type}'."
            )

        self._interface_manager = interface_manager or ConsoleInterfaceManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._config_manager = config_manager or ConfigManager()

    def execute(self) -> None:
        father_place_templates: Optional[dict]

        if self._father_place_template_type == TemplateType.WORLD:
            father_place_templates = (
                self._filesystem_manager.load_existing_or_new_json_file(
                    WORLD_TEMPLATES_FILE
                )
            )
        elif self._father_place_template_type == TemplateType.REGION:
            father_place_templates = (
                self._filesystem_manager.load_existing_or_new_json_file(
                    REGIONS_TEMPLATES_FILE
                )
            )
        elif self._father_place_template_type == TemplateType.AREA:
            father_place_templates = (
                self._filesystem_manager.load_existing_or_new_json_file(
                    AREAS_TEMPLATES_FILE
                )
            )
        else:
            raise ValueError(
                f"Wasn't programmed to load the templates for template type '{self._place_template_type}'."
            )

        if self._father_place_name not in father_place_templates:
            raise ValueError(
                f"There isn't a {self._place_template_type} template named '{self._father_place_name}'"
            )

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, self._config_manager.get_heavy_llm()
        )

        llm_tool_response_product = PlaceGenerationToolResponseProvider(
            self._father_place_name,
            self._place_template_type,
            self._notion,
            produce_tool_response_strategy_factory,
        ).generate_product()

        if not llm_tool_response_product.is_valid():
            raise ValueError(
                f"Was unable to produce a tool response for {self._place_template_type.value} generation: {llm_tool_response_product.get_error()}"
            )

        # Extract area data using the function provided
        place_data = llm_tool_response_product.get()

        # Make them lowercase.
        place_data.update(
            {
                "categories": [
                    category.lower()
                    for category in father_place_templates[self._father_place_name][
                        "categories"
                    ]
                ]
            }
        )

        StoreGeneratedPlaceCommand(
            place_data, template_type=self._place_template_type
        ).execute()
