import logging
import logging.config
from typing import Optional

from src.abstracts.command import Command
from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import RandomPlaceTemplateBasedOnCategoriesFactory
from src.maps.commands.create_map_entry_for_playthrough_command import CreateMapEntryForPlaythroughCommand
from src.maps.map_manager import MapManager

logger = logging.getLogger(__name__)


class CreateRandomPlaceTypeMapEntryForPlaythroughCommand(Command):
    def __init__(self, playthrough_name: str, father_identifier: Optional[str], father_template: str,
                 place_type: PlaceType, father_place_type: PlaceType,
                 random_place_template_based_on_categories_factory: RandomPlaceTemplateBasedOnCategoriesFactory,
                 filesystem_manager: FilesystemManager = None, map_manager: MapManager = None):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")
        if not father_template:
            raise ValueError("'father_template' can't be empty.")
        if not random_place_template_based_on_categories_factory:
            raise ValueError("'random_place_template_based_on_categories_factory' can't be empty.")

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._father_template = father_template
        self._place_type = place_type
        self._father_place_type = father_place_type
        self._random_place_template_based_on_categories_factory = random_place_template_based_on_categories_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._map_manager = map_manager or MapManager(playthrough_name)

        logging.config.dictConfig(self._filesystem_manager.get_logging_config_file())

    def execute(self) -> None:
        if self._place_type == PlaceType.REGION:
            place_templates_file_path = self._filesystem_manager.get_file_path_to_regions_template_file()
        elif self._place_type == PlaceType.AREA:
            place_templates_file_path = self._filesystem_manager.get_file_path_to_areas_template_file()
        elif self._place_type == PlaceType.LOCATION:
            place_templates_file_path = self._filesystem_manager.get_file_path_to_locations_template_file()
        else:
            raise NotImplementedError(
                "Haven't programmed in how to create map entries anything other than regions for now.")

        template_product = self._random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories(
            self._filesystem_manager.load_existing_or_new_json_file(
                place_templates_file_path),
            self._map_manager.get_place_categories(
                self._father_template, self._father_place_type))

        if not template_product.is_valid():
            raise ValueError(
                f"Wasn't able to produce a {self._place_type.value} template: {template_product.get_error()}")

        CreateMapEntryForPlaythroughCommand(self._playthrough_name, self._father_identifier, self._place_type,
                                            template_product.get()).execute()
