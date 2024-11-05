from src.base.validators import validate_non_empty_string
from src.maps.commands.attach_place_command import AttachPlaceCommand
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class AttachPlaceCommandFactory:
    def __init__(
        self, playthrough_name: str, place_manager_factory: PlaceManagerFactory
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._place_manager_factory = place_manager_factory

    def create_command(self, map_entry_identifier: str) -> AttachPlaceCommand:
        return AttachPlaceCommand(
            self._playthrough_name,
            map_entry_identifier,
            self._place_manager_factory.create_place_manager(),
        )
