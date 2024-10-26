import logging
from pathlib import Path

from src.base.abstracts.command import Command
from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.filesystem.file_operations import read_json_file, write_json_file
from src.maps.place_data import PlaceData

logger = logging.getLogger(__name__)


class StoreGeneratedPlaceCommand(Command):

    def __init__(
        self,
        place_data: PlaceData,
        template_type: TemplateType,
    ):
        self._place_data = place_data
        self._template_type = template_type

    def _add_place_data_to_templates_file(self, current_places_template_file):
        current_places_template_file.update(
            {
                self._place_data.name: {
                    "description": self._place_data.description,
                    "categories": [
                        category.lower() for category in self._place_data.categories
                    ],
                }
            }
        )

    def _handle_location_type(self, current_places_template_file):
        if self._template_type == TemplateType.LOCATION:
            if not self._place_data.type:
                raise KeyError(
                    "Was tasked with storing a location, but the place data didn't contain the 'type' key."
                )
            current_places_template_file[self._place_data.name][
                "type"
            ] = self._place_data.type

    def execute(self) -> None:
        current_places_template_file = read_json_file(
            Path(TEMPLATE_FILES.get(self._template_type))
        )

        self._add_place_data_to_templates_file(current_places_template_file)

        self._handle_location_type(current_places_template_file)

        write_json_file(
            Path(TEMPLATE_FILES.get(self._template_type)), current_places_template_file
        )

        logger.info(f"Saved {self._template_type} template '{self._place_data.name}'.")
