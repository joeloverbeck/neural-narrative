from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import PARENT_KEYS
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.filesystem.path_manager import PathManager
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_repository import MapRepository


class ExitPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        visit_place_command_factory: VisitPlaceCommandFactory,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_repository: Optional[MapRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._visit_place_command_factory = visit_place_command_factory
        self._place_manager_factory = place_manager_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_repository = map_repository or MapRepository(self._playthrough_name)
        self._path_manager = path_manager or PathManager()

    def execute(self) -> None:
        place_manager = self._place_manager_factory.create_place_manager()

        current_place_type = place_manager.get_current_place_type()

        if (
            current_place_type != TemplateType.LOCATION
            and current_place_type != TemplateType.ROOM
        ):
            raise ValueError(
                f"Somehow tried to exit a location when the current place wasn't a location nor a room. Current place type: '{current_place_type}'."
            )

        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )

        map_file = self._map_repository.load_map_data()

        destination_area = map_file[current_place_identifier][
            PARENT_KEYS.get(current_place_type)
        ]

        self._visit_place_command_factory.create_visit_place_command(
            destination_area
        ).execute()
