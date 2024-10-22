import logging
from typing import Optional
from src.base.abstracts.command import Command
from src.base.constants import TEMPLATE_FILES
from src.base.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.place_data import PlaceData
logger = logging.getLogger(__name__)


class StoreGeneratedPlaceCommand(Command):

    def __init__(self, place_data: PlaceData, template_type: TemplateType,
                 filesystem_manager: Optional[FilesystemManager] = None):
        self._place_data = place_data
        self._template_type = template_type
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        current_places_template_file: Optional[dict]
        current_places_template_file = (self._filesystem_manager.
                                        load_existing_or_new_json_file(TEMPLATE_FILES.get(self.
                                                                                          _template_type)))
        current_places_template_file.update({self._place_data.name: {
            'description': self._place_data.description, 'categories': [
                category.lower() for category in self._place_data.categories]}})
        if self._template_type == TemplateType.LOCATION:
            if not self._place_data.type:
                raise KeyError(
                    "Was tasked with storing a location, but the place data didn't contain the 'type' key."
                )
            current_places_template_file[self._place_data.name]['type'
            ] = self._place_data.type
        self._filesystem_manager.save_json_file(current_places_template_file,
                                                TEMPLATE_FILES.get(self._template_type))
        logger.info(
            f"Saved {self._template_type} template '{self._place_data.name}'.")
