from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.characters.characters_manager import CharactersManager
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory


class GeneratePlayerCharacterCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        user_content: str,
        generate_character_command_factory: GenerateCharacterCommandFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        playthrough_manager: PlaythroughManager = None,
        characters_manager: CharactersManager = None,
    ):
        self._user_content = user_content
        self._generate_character_command_factory = generate_character_command_factory
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def execute(self) -> None:
        places_parameter = self._hierarchy_manager_factory.create_hierarchy_manager().fill_places_templates_parameter(
            self._playthrough_manager.get_current_place_identifier()
        )
        self._generate_character_command_factory.create_generate_character_command(
            places_parameter,
            place_character_at_current_place=False,
            user_content=self._user_content,
        ).execute()
        self._playthrough_manager.update_player_identifier(
            self._characters_manager.get_latest_character_identifier()
        )
