from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.characters.factories.generate_random_characters_command_factory import (
    GenerateRandomCharactersCommandFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.config.config_manager import ConfigManager
from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


class PlaceService:
    def __init__(self, config_manager: ConfigManager = None):
        self._config_manager = config_manager or ConfigManager()

    def describe_place(self, playthrough_name):
        playthrough_manager = PlaythroughManager(playthrough_name)
        llm_client = OpenRouterLlmClientFactory().create_llm_client()
        strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, self._config_manager.get_heavy_llm()
        )
        description_product = ConcreteFilteredPlaceDescriptionGenerationFactory(
            playthrough_name,
            playthrough_manager.get_player_identifier(),
            playthrough_manager.get_current_place_identifier(),
            strategy_factory,
        ).generate_filtered_place_description()

        if description_product.is_valid():
            return description_product.get()
        else:
            return description_product.get_error()

    def exit_location(self, playthrough_name):
        playthrough_manager = PlaythroughManager(playthrough_name)
        filesystem_manager = FilesystemManager()
        map_manager = MapManager(playthrough_name)

        if not map_manager.get_current_place_type() == PlaceType.LOCATION:
            raise ValueError(
                "Somehow tried to exit a location when the current place wasn't a location."
            )

        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(playthrough_name)
        )
        current_place_identifier = playthrough_manager.get_current_place_identifier()
        destination_area = map_file[current_place_identifier]["area"]

        visit_command_factory = self._create_visit_place_command_factory(
            playthrough_name
        )
        visit_command_factory.create_visit_place_command(destination_area).execute()

    def visit_location(self, playthrough_name, location_identifier):
        visit_command_factory = self._create_visit_place_command_factory(
            playthrough_name
        )
        visit_command_factory.create_visit_place_command(location_identifier).execute()

    def _create_visit_place_command_factory(self, playthrough_name):
        strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            self._config_manager.get_heavy_llm(),
        )
        store_character_factory = StoreGeneratedCharacterCommandFactory(
            playthrough_name
        )
        image_command_factory = GenerateCharacterImageCommandFactory(
            playthrough_name,
            OpenAIGeneratedImageFactory(OpenAILlmClientFactory().create_llm_client()),
            ConcreteUrlContentFactory(),
        )
        character_command_factory = GenerateCharacterCommandFactory(
            playthrough_name,
            strategy_factory,
            store_character_factory,
            image_command_factory,
        )
        random_characters_factory = GenerateRandomCharactersCommandFactory(
            playthrough_name, character_command_factory
        )

        return VisitPlaceCommandFactory(
            playthrough_name, random_characters_factory, strategy_factory
        )
