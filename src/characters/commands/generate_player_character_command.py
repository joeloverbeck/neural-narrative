from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager


class GeneratePlayerCharacterCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        user_content: str,
        generate_character_command_factory: GenerateCharacterCommandFactory,
        map_manager: MapManager = None,
        playthrough_manager: PlaythroughManager = None,
        characters_manager: CharactersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._user_content = user_content
        self._generate_character_command_factory = generate_character_command_factory

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        places_parameter = self._map_manager.fill_places_templates_parameter(
            self._playthrough_manager.get_current_place_identifier()
        )

        # Now should create the player character.
        self._generate_character_command_factory.create_generate_character_command(
            places_parameter,
            place_character_at_current_place=False,
            user_content=self._user_content,
        ).execute()

        self._playthrough_manager.update_player_identifier(
            self._characters_manager.get_latest_character_identifier()
        )
