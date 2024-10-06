import logging
from typing import Optional

from src.abstracts.command import Command
from src.constants import (
    WORLD_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class StoreGeneratedPlaceCommand(Command):
    def __init__(
        self,
        place_data: dict,
        template_type: TemplateType,
        filesystem_manager: FilesystemManager = None,
    ):
        if not isinstance(place_data, dict):
            raise TypeError(
                f"place_data should have been a dict, but was '{type(place_data)}'."
            )

        self._place_data = place_data
        self._template_type = template_type

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        # Have to load the corresponding place templates file
        current_places_template_file: Optional[dict]

        file_path: Optional[str]

        if self._template_type == TemplateType.WORLD:
            file_path = WORLD_TEMPLATES_FILE
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.REGION:
            file_path = REGIONS_TEMPLATES_FILE
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.AREA:
            file_path = AREAS_TEMPLATES_FILE
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.LOCATION:
            file_path = LOCATIONS_TEMPLATES_FILE
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        else:
            raise ValueError(
                f"Wasn't programmed to load the templates file of template '{self._template_type}'."
            )

        # Make the categories lowercase
        current_places_template_file.update(
            {
                self._place_data["name"]: {
                    "description": self._place_data["description"],
                    "categories": [
                        category.lower() for category in self._place_data["categories"]
                    ],
                }
            }
        )

        self._filesystem_manager.save_json_file(current_places_template_file, file_path)

        logger.info(
            f"Saved {self._template_type.value} template '{self._place_data["name"]}'."
        )
