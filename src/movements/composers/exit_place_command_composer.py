from src.base.validators import validate_non_empty_string
from src.maps.composers.visit_place_command_factory_composer import (
    VisitPlaceCommandFactoryComposer,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.exit_place_command import ExitPlaceCommand


class ExitPlaceCommandComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_command(self) -> ExitPlaceCommand:
        visit_place_command_factory = VisitPlaceCommandFactoryComposer(
            self._playthrough_name
        ).compose_factory()
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        return ExitPlaceCommand(
            self._playthrough_name, visit_place_command_factory, place_manager_factory
        )
