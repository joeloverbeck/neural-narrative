from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.visit_place_command import VisitPlaceCommand
from src.movements.factories.process_first_visit_to_place_command_factory import (
    ProcessFirstVisitToPlaceCommandFactory,
)


class VisitPlaceCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        process_first_visit_to_place_command_factory: ProcessFirstVisitToPlaceCommandFactory,
        place_manager_factory: PlaceManagerFactory,
    ):
        self._playthrough_name = playthrough_name
        self._process_first_visit_to_place_command_factory = (
            process_first_visit_to_place_command_factory
        )
        self._place_manager_factory = place_manager_factory

    def create_visit_place_command(self, place_identifier: str) -> VisitPlaceCommand:
        return VisitPlaceCommand(
            self._playthrough_name,
            place_identifier,
            self._process_first_visit_to_place_command_factory,
            self._place_manager_factory,
        )
