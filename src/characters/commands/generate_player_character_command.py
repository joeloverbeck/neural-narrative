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
        self._generate_character_command_factory.create_generate_character_command(
            is_player=True,
            user_content=self._user_content,
        ).execute()
        self._playthrough_manager.update_player_identifier(
            self._characters_manager.get_latest_character_identifier()
        )
