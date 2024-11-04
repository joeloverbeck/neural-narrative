from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import CHILDREN_KEYS
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.filesystem.config_loader import ConfigLoader
from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.time.time_manager import TimeManager


class AttachPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        map_entry_identifier: str,
        place_manager: PlaceManager,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_repository: Optional[MapRepository] = None,
        time_manager: Optional[TimeManager] = None,
        config_loader: Optional[ConfigLoader] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(map_entry_identifier, "map_entry_identifier")

        self._map_entry_identifier = map_entry_identifier
        self._place_manager = place_manager

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._map_repository = map_repository or MapRepository(playthrough_name)
        self._time_manager = time_manager or TimeManager(playthrough_name)
        self._config_loader = config_loader or ConfigLoader()

    def execute(self) -> None:
        current_place_type = self._place_manager.get_current_place_type()

        if (
            current_place_type != TemplateType.AREA
            and current_place_type != TemplateType.LOCATION
        ):
            raise ValueError(
                f"Attempted to attach a place to the current place type, that is neither an area nor a location: '{current_place_type}'."
            )

        map_file = self._map_repository.load_map_data()

        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )

        children_key = CHILDREN_KEYS.get(current_place_type)

        if (
            self._map_entry_identifier
            in map_file[current_place_identifier][children_key]
        ):
            raise ValueError(
                f"Map entry identifier '{self._map_entry_identifier}' already present in the {children_key} of the current {current_place_type}."
            )

        map_file[current_place_identifier][children_key].append(
            self._map_entry_identifier
        )

        self._map_repository.save_map_data(map_file)

        self._time_manager.advance_time(
            self._config_loader.get_time_advanced_due_to_searching_for_location()
        )
