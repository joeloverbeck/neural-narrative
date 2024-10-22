from src.base.abstracts.command import Command
from src.base.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory


class CreatePlaythroughCommand(Command):
    """Command to create a new playthrough with a specified world template."""

    def __init__(
        self,
        create_playthrough_metadata_command: CreatePlaythroughMetadataCommand,
        create_initial_map_command: CreateInitialMapCommand,
        generate_player_character_command: GeneratePlayerCharacterCommand,
        visit_place_command_factory: VisitPlaceCommandFactory,
            map_manager_factory: MapManagerFactory,
    ):
        self._create_playthrough_metadata_command = create_playthrough_metadata_command
        self._create_initial_map_command = create_initial_map_command
        self._generate_player_character_command = generate_player_character_command
        self._visit_place_command_factory = visit_place_command_factory
        self._map_manager_factory = map_manager_factory

    def execute(self) -> None:
        self._create_playthrough_metadata_command.execute()
        self._create_initial_map_command.execute()
        latest_identifier, _ = (
            self._map_manager_factory.create_map_manager().get_identifier_and_place_template_of_latest_map_entry()
        )
        self._visit_place_command_factory.create_visit_place_command(
            latest_identifier
        ).execute()
        self._generate_player_character_command.execute()
