import logging
import logging.config
from typing import Optional

from src.abstracts.command import Command
from src.enums import PlaceType, IdentifierType
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager

logger = logging.getLogger(__name__)


class CreateMapEntryForPlaythroughCommand(Command):
    def __init__(self, playthrough_name: str, father_identifier: Optional[str], place_type: PlaceType,
                 place_template: str,
                 filesystem_manager: FilesystemManager = None,
                 identifiers_manager: IdentifiersManager = None):
        if not playthrough_name:
            raise ValueError("'playthrough_name' can't be empty.")
        if not place_type:
            raise ValueError("'place_type' can't be empty.")
        if not place_template:
            raise ValueError("'place_template' can't be empty.")

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type
        self._place_template = place_template
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(self._playthrough_name)

        logging.config.dictConfig(self._filesystem_manager.get_logging_config_file())

    def execute(self) -> None:
        """Create a map entry for the playthrough using the selected place."""

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        # need to create the next identifier for the place.
        new_id = self._identifiers_manager.produce_and_update_next_identifier(IdentifierType.PLACES)

        # We have the corresponding map file. What to do now depends on the type of place to create
        if self._place_type == PlaceType.REGION:
            # The map entry should have 'type' and 'place_template'.
            map_file.update({
                str(new_id): {
                    "type": self._place_type.value,
                    "place_template": self._place_template
                }
            })
        elif self._place_type == PlaceType.AREA:
            # the map entry should have 'type', 'place_template', 'region', 'locations', and 'characters'
            if not self._father_identifier:
                raise ValueError(
                    "When creating a map entry for an area, found out that the command hadn't received the father's identifier.")

            map_file.update({
                str(new_id): {
                    "type": self._place_type.value,
                    "place_template": self._place_template,
                    "region": self._father_identifier,
                    "locations": [],
                    "characters": []
                }
            })
        elif self._place_type == PlaceType.LOCATION:
            # the map entry should have 'type', 'place_template', 'area', and 'characters'
            if not self._father_identifier:
                raise ValueError(
                    "When creating a map entry for a location, found out that the command hadn't received the father's identifier.")

            map_file.update({
                str(new_id): {
                    "type": self._place_type.value,
                    "place_template": self._place_template,
                    "area": self._father_identifier,
                    "characters": []
                }
            })
        else:
            raise ValueError(f"This function wasn't programmed to handle place type '{self._place_type}'.")

        # save the map back to file
        self._filesystem_manager.save_json_file(map_file,
                                                self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        logger.info(
            f"Map created for playthrough '{self._playthrough_name}' with {self._place_type.value} '{self._place_template}'.")
