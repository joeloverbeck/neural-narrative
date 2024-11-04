from typing import Optional

from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.filesystem.config_loader import ConfigLoader
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.factories.process_first_visit_to_place_command_factory import (
    ProcessFirstVisitToPlaceCommandFactory,
)
from src.time.time_manager import TimeManager


class VisitPlaceCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        process_first_visit_to_place_command_factory: ProcessFirstVisitToPlaceCommandFactory,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        time_manager: Optional[TimeManager] = None,
        config_loader: Optional[ConfigLoader] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(place_identifier, "place_identifier")

        self._place_identifier = place_identifier
        self._process_first_visit_to_place_command_factory = (
            process_first_visit_to_place_command_factory
        )
        self._place_manager_factory = place_manager_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._time_manager = time_manager or TimeManager(playthrough_name)
        self._config_loader = config_loader or ConfigLoader()

    def execute(self) -> None:
        self._playthrough_manager.update_current_place(self._place_identifier)

        # The following will only get done if the current place isn't a room.
        place_manager = self._place_manager_factory.create_place_manager()

        if place_manager.get_current_place_type() == TemplateType.ROOM:
            return

        if not place_manager.is_visited(self._place_identifier):
            self._process_first_visit_to_place_command_factory.create_command(
                self._place_identifier
            ).execute()

        self._time_manager.advance_time(
            self._config_loader.get_time_advanced_due_to_exiting_location()
        )
