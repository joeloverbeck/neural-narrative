from src.abstracts.command import Command
from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager


class CreatePlaythroughCommand(Command):
    """Command to create a new playthrough with a specified world template."""

    def __init__(
        self,
        playthrough_name: str,
        world_template: str,
        create_playthrough_metadata_command: CreatePlaythroughMetadataCommand,
        create_initial_map_command: CreateInitialMapCommand,
        generate_player_character_command: GeneratePlayerCharacterCommand,
        visit_place_command_factory: VisitPlaceCommandFactory,
        map_manager: MapManager = None,
        playthrough_manager: PlaythroughManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not world_template:
            raise ValueError("world_template must not be empty.")
        if not create_playthrough_metadata_command:
            raise ValueError("create_playthrough_metadata_command must not be empty.")
        if not create_initial_map_command:
            raise ValueError("initial_map_command must not be empty.")
        if not generate_player_character_command:
            raise ValueError("generate_initial_characters_command can't be empty.")

        self._playthrough_name = playthrough_name
        self._create_playthrough_metadata_command = create_playthrough_metadata_command
        self._create_initial_map_command = create_initial_map_command
        self._generate_player_character_command = generate_player_character_command
        self._visit_place_command_factory = visit_place_command_factory

        self._map_manager = map_manager or MapManager(playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        # First create the playthrough metadata.
        self._create_playthrough_metadata_command.execute()

        # Next, we have to create the initial map.
        self._create_initial_map_command.execute()

        # Now let's update in the playthrough metadata the current place as the latest location created.
        latest_identifier, _ = (
            self._map_manager.get_identifier_and_place_template_of_latest_map_entry()
        )

        # Visit the latest place created. The visitation is responsible for generating new characters.
        self._visit_place_command_factory.create_visit_place_command(
            latest_identifier
        ).execute()

        # Generate player character.
        self._generate_player_character_command.execute()
