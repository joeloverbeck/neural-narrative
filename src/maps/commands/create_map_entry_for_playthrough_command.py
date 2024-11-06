import logging.config
from typing import Optional, Dict, Any

from src.base.abstracts.command import Command
from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.constants import PARENT_KEYS
from src.base.enums import TemplateType
from src.base.identifiers_manager import IdentifiersManager
from src.base.validators import validate_non_empty_string
from src.filesystem.path_manager import PathManager
from src.maps.map_repository import MapRepository

logger = logging.getLogger(__name__)


class CreateMapEntryForPlaythroughCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        father_identifier: Optional[str],
        place_type: TemplateType,
        place_template: str,
        produce_and_update_next_identifier: ProduceAndUpdateNextIdentifierAlgorithm,
        identifiers_manager: Optional[IdentifiersManager] = None,
        map_repository: Optional[MapRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(place_template, "place_template")
        if not isinstance(place_type, TemplateType):
            raise TypeError(
                f"Expected 'place_type' to be a TemplateType, but was '{type(place_type)}'."
            )

        self._playthrough_name = playthrough_name
        self._father_identifier = father_identifier
        self._place_type = place_type
        self._place_template = place_template
        self._produce_and_update_next_identifier = produce_and_update_next_identifier

        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )
        self._map_repository = map_repository or MapRepository(self._playthrough_name)
        self._path_manager = path_manager or PathManager()

    def _get_parent_key(self) -> Optional[str]:
        """Get the parent key based on the place type."""
        return PARENT_KEYS.get(self._place_type)

    def _get_additional_fields(self) -> Dict[str, Any]:
        """Get additional fields required based on the place type."""
        additional_fields: Dict[str, Any] = {}
        if self._place_type == TemplateType.AREA:
            additional_fields.update(
                {
                    "weather_identifier": "sunny",
                    "locations": [],
                    "characters": [],
                    "visited": False,
                }
            )
        elif self._place_type == TemplateType.LOCATION:
            additional_fields.update({"characters": [], "rooms": [], "visited": False})
        elif self._place_type == TemplateType.ROOM:
            additional_fields.update({"characters": []})
        return additional_fields

    def execute(self) -> None:
        """Create a map entry for the playthrough using the selected place."""
        map_file = self._map_repository.load_map_data()

        new_id = self._produce_and_update_next_identifier.do_algorithm()

        map_entry = {
            "type": self._place_type.value,
            "place_template": self._place_template,
        }

        parent_key = self._get_parent_key()

        if parent_key:
            if not self._father_identifier:
                raise ValueError(
                    f"When creating a map entry for '{self._place_type}', the father's identifier is required but was not provided."
                )
            map_entry[parent_key] = self._father_identifier

        additional_fields = self._get_additional_fields()
        map_entry.update(additional_fields)

        # If for whatever reason we don't get a map, may as well initialize it here.
        if not map_file:
            map_file = {}

        map_file[str(new_id)] = map_entry

        self._map_repository.save_map_data(map_file)

        logger.info(
            f"Map entry created for playthrough '{self._playthrough_name}' with {self._place_type.value} '{self._place_template}'."
        )
