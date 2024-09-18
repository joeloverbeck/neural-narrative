from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.commands.generate_random_characters_command import (
    GenerateRandomCharactersCommand,
)
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.automatic_user_content_for_character_generation_factory import (
    AutomaticUserContentForCharacterGenerationFactory,
)
from src.prompting.factories.player_guided_user_content_for_character_generation_factory import (
    PlayerGuidedUserContentForCharacterGenerationFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.requests.abstracts.abstract_factories import UrlContentFactory


class GenerateInitialCharactersCommand(Command):
    def __init__(
            self,
            playthrough_name: str,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            generated_image_factory: GeneratedImageFactory,
            url_content_factory: UrlContentFactory,
            map_manager: MapManager = None,
            playthrough_manager: PlaythroughManager = None,
            characters_manager: CharactersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not generated_image_factory:
            raise ValueError("generated_image_factory can't be empty.")
        if not url_content_factory:
            raise ValueError("url_content_factory can't be empty.")

        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        places_parameter = self._map_manager.fill_places_parameter(
            self._playthrough_manager.get_current_place_identifier()
        )

        # Now should create the player character.
        GenerateCharacterCommand(
            self._playthrough_name,
            places_parameter,
            self._produce_tool_response_strategy_factory,
            PlayerGuidedUserContentForCharacterGenerationFactory(),
            self._generated_image_factory,
            self._url_content_factory,
        ).execute()

        self._playthrough_manager.update_player_identifier(
            self._characters_manager.get_latest_character_identifier()
        )

        # Now delegate creating a few characters at the location.
        GenerateRandomCharactersCommand(
            self._playthrough_name,
            GenerateCharacterCommand(
                self._playthrough_name,
                places_parameter,
                self._produce_tool_response_strategy_factory,
                AutomaticUserContentForCharacterGenerationFactory(),
                self._generated_image_factory,
                self._url_content_factory,
            ),
        ).execute()
