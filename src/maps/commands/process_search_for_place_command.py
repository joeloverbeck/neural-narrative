from src.base.abstracts.command import Command
from src.maps.commands.search_for_place_command import SearchForPlaceCommand
from src.maps.factories.attach_place_command_factory import AttachPlaceCommandFactory
from src.maps.factories.map_manager_factory import MapManagerFactory


class ProcessSearchForPlaceCommand(Command):
    def __init__(
        self,
        search_for_place_command: SearchForPlaceCommand,
        attach_place_command_factory: AttachPlaceCommandFactory,
        map_manager_factory: MapManagerFactory,
    ):
        self._search_for_place_command = search_for_place_command
        self._attach_place_command_factory = attach_place_command_factory
        self._map_manager_factory = map_manager_factory

    def execute(self) -> None:
        self._search_for_place_command.execute()

        new_id, _ = (
            self._map_manager_factory.create_map_manager().get_identifier_and_place_template_of_latest_map_entry()
        )

        self._attach_place_command_factory.create_command(new_id).execute()
