import logging
from typing import Optional, Dict, Callable, Type

from pydantic import BaseModel

from src.base.abstracts.command import Command
from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.models.area import Area
from src.maps.models.location import get_custom_location_class
from src.maps.models.region import Region
from src.maps.models.world import World
from src.maps.place_data import PlaceData
from src.maps.templates_repository import TemplatesRepository
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)

logger = logging.getLogger(__name__)


class GeneratePlaceCommand(Command):
    """
    Command to generate a new place based on a given template type and its parent place.
    """

    PLACE_TYPE_TO_CLASS: Dict[TemplateType, Callable[[], Type[BaseModel]]] = {
        TemplateType.LOCATION: get_custom_location_class,
        TemplateType.AREA: lambda: Area,
        TemplateType.REGION: lambda: Region,
        TemplateType.WORLD: lambda: World,
    }

    def _validate_parent_template_type(self) -> None:
        """
        Validate that the father place template type is the expected parent of the place template type.
        """
        expected_parent = PARENT_TEMPLATE_TYPE.get(self._place_template_type)
        if expected_parent is None:
            raise ValueError(
                f"Invalid place_template_type: '{self._place_template_type.value}'"
            )
        if self._father_place_template_type != expected_parent:
            raise ValueError(
                f"Attempted to create a '{self._place_template_type.value}' from something other than a '{expected_parent.value}'! The parent place was '{self._father_place_template_type.value}'."
            )

    def _get_father_place_data(self) -> Dict:
        """
        Retrieve the father place data from the templates repository.

        Returns:
            Dict: The father place data.
        """
        father_place_templates = self._templates_repository.load_templates(
            self._father_place_template_type
        )

        if self._father_place_name not in father_place_templates:
            raise ValueError(
                f"There isn't a '{self._father_place_template_type}' template named '{self._father_place_name}'."
            )
        return father_place_templates[self._father_place_name]

    def _get_categories(self, father_place_data: Dict) -> list:
        """
        Retrieve and validate the categories from the father place data.

        Args:
            father_place_data (Dict): The father place data.

        Returns:
            list: A list of categories.
        """
        categories = father_place_data.get("categories", [])
        if not categories:
            raise ValueError(
                f"There were no categories for father place '{self._father_place_name}'."
            )
        return [category.lower() for category in categories]

    def _get_place_class(self) -> Type[BaseModel]:
        """
        Retrieve the class corresponding to the place template type.

        Returns:
            type: The class for the place template type.
        """
        place_class_callable = self.PLACE_TYPE_TO_CLASS.get(self._place_template_type)
        if place_class_callable is None:
            raise NotImplementedError(
                f"Product generation not implemented for template type '{self._place_template_type}'."
            )
        return place_class_callable()

    def __init__(
        self,
        place_template_type: TemplateType,
        father_place_template_type: TemplateType,
        father_place_name: str,
        place_generation_tool_response_provider: PlaceGenerationToolResponseProvider,
        store_generated_place_command_factory: StoreGeneratedPlaceCommandFactory,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        """
        Initialize the GeneratePlaceCommand.

        Args:
            place_template_type (TemplateType): The type of place to generate.
            father_place_template_type (TemplateType): The type of the parent place.
            father_place_name (str): The name of the parent place.
            place_generation_tool_response_provider (PlaceGenerationToolResponseProvider): Provider for generating the place data.
            store_generated_place_command_factory (StoreGeneratedPlaceCommandFactory): Factory for storing the generated place.
        """
        validate_non_empty_string(father_place_name, "father_place_name")

        self._place_template_type = place_template_type
        self._father_place_template_type = father_place_template_type
        self._father_place_name = father_place_name
        self._place_generation_tool_response_provider = (
            place_generation_tool_response_provider
        )
        self._store_generated_place_command_factory = (
            store_generated_place_command_factory
        )

        self._templates_repository = templates_repository or TemplatesRepository()

        self._validate_parent_template_type()

    def execute(self) -> None:
        """
        Execute the command to generate and store the new place.
        """
        father_place_data = self._get_father_place_data()
        place_class = self._get_place_class()

        llm_tool_response_product = (
            self._place_generation_tool_response_provider.generate_product(place_class)
        )

        if not llm_tool_response_product.is_valid():
            raise ValueError(
                f"Unable to produce a tool response for '{self._place_template_type.value}' generation: {llm_tool_response_product.get_error()}"
            )

        categories = self._get_categories(father_place_data)

        response_dict = llm_tool_response_product.get()
        type_data = response_dict.get("type")
        place_data = PlaceData(
            response_dict["name"],
            response_dict["description"].replace("\n\n", "\n"),
            categories,
            type_data,
        )

        self._store_generated_place_command_factory.create_command(place_data).execute()
