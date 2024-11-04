import logging
from typing import Optional

from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.maps.place_data import PlaceData
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class StoreGeneratedPlaceCommand(Command):

    def __init__(
        self,
        place_data: PlaceData,
        template_type: TemplateType,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        self._place_data = place_data
        self._template_type = template_type

        self._templates_repository = templates_repository or TemplatesRepository()

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
        # Locations and Rooms should have a type.
        if (
            self._template_type == TemplateType.LOCATION
            or self._template_type == TemplateType.ROOM
        ):
            if not self._place_data.type:
                raise KeyError(
                    f"Was tasked with storing a {self._template_type.value}, but the place data didn't contain the 'type' key."
                )
            current_places_template_file[self._place_data.name][
                "type"
            ] = self._place_data.type

    def execute(self) -> None:
        current_places_template_file = self._templates_repository.load_templates(
            self._template_type
        )

        self._add_place_data_to_templates_file(current_places_template_file)

        self._handle_location_type(current_places_template_file)

        self._templates_repository.save_templates(
            self._template_type, current_places_template_file
        )

        logger.info(f"Saved {self._template_type} template '{self._place_data.name}'.")
