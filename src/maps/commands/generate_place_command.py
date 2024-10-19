import logging
from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import TEMPLATE_FILES, PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.playthrough_name import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.place_data import PlaceData
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)

logger = logging.getLogger(__name__)


class GeneratePlaceCommand(Command):
    """
    Command to generate a new place based on a given template type and its parent place.
    """

    def __init__(
        self,
        place_template_type: TemplateType,
        father_place_template_type: TemplateType,
        father_place_name: RequiredString,
        place_generation_tool_response_provider: PlaceGenerationToolResponseProvider,
        store_generated_place_command_factory: StoreGeneratedPlaceCommandFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        """
        Initialize the GeneratePlaceCommand.

        Args:
            place_template_type (TemplateType): The type of place to generate.
            father_place_template_type (TemplateType): The type of the parent place.
            father_place_name (RequiredString): The name of the parent place.
            place_generation_tool_response_provider (PlaceGenerationToolResponseProvider): Provider for generating the place data.
            filesystem_manager (Optional[FilesystemManager], optional): Filesystem manager instance. Defaults to FilesystemManager.
        """
        if not father_place_name:
            raise ValueError("father_place_name can't be empty.")

        self._place_template_type = place_template_type
        self._father_place_template_type = father_place_template_type
        self._father_place_name = father_place_name
        self._place_generation_tool_response_provider = (
            place_generation_tool_response_provider
        )
        self._store_generated_place_command_factory = (
            store_generated_place_command_factory
        )

        # Sanity check for correct parent place type
        expected_parent = PARENT_TEMPLATE_TYPE.get(self._place_template_type)
        if expected_parent is None:
            raise ValueError(
                f"Invalid place_template_type: '{self._place_template_type.value}'"
            )
        if self._father_place_template_type != expected_parent:
            raise ValueError(
                f"Attempted to create a '{self._place_template_type.value}' from something other than a '{expected_parent.value}'! "
                f"The parent place was '{self._father_place_template_type.value}'."
            )

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        """
        Execute the command to generate and store the new place.
        """
        # Load parent place templates
        father_template_file = TEMPLATE_FILES.get(self._father_place_template_type)
        if not father_template_file:
            raise ValueError(
                f"Unrecognized father_place_template_type '{self._father_place_template_type.value}'."
            )

        father_place_templates = (
            self._filesystem_manager.load_existing_or_new_json_file(
                father_template_file
            )
        )

        if self._father_place_name.value not in father_place_templates:
            raise ValueError(
                f"There isn't a '{self._father_place_template_type.value}' template named '{self._father_place_name.value}'."
            )

        # Generate the place data
        llm_tool_response_product = (
            self._place_generation_tool_response_provider.generate_product()
        )

        if not llm_tool_response_product.is_valid():
            raise ValueError(
                f"Unable to produce a tool response for '{self._place_template_type.value}' generation: "
                f"{llm_tool_response_product.get_error()}"
            )

        # Extract and process place data
        father_place_data = father_place_templates[self._father_place_name.value]
        categories = father_place_data.get("categories", [])

        if not categories:
            raise ValueError(
                f"There were no categories for father place '{self._father_place_name}'."
            )

        response_dict = llm_tool_response_product.get()

        type_data = (
            RequiredString(response_dict["type"]) if "type" in response_dict else None
        )

        place_data = PlaceData(
            RequiredString(response_dict["name"]),
            RequiredString(response_dict["description"].replace("\n\n", "\n")),
            [RequiredString(category.lower()) for category in categories],
            type_data,
        )

        # Store the generated place
        self._store_generated_place_command_factory.create_command(place_data).execute()
