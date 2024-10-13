from typing import Optional

from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.config.config_manager import ConfigManager
from src.enums import PlaceType, TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_manager import MapManager
from src.maps.strategies.fathered_place_generation_strategy import (
    FatheredPlaceGenerationStrategy,
)
from src.maps.strategies.world_generation_strategy import WorldGenerationStrategy
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.voices.voice_manager import VoiceManager


class PlaceService:
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        voice_manager: Optional[VoiceManager] = None,
    ):
        self._config_manager = config_manager or ConfigManager()
        self._voice_manager = voice_manager or VoiceManager()

    def _generate_place_description_voice_line(
        self, playthrough_name, description_text
    ):

        # Load the player's voice model.
        player = Character(
            playthrough_name,
            PlaythroughManager(playthrough_name).get_player_identifier(),
        )

        return self._voice_manager.generate_voice_line(
            player.name, description_text, player.voice_model
        )

    def describe_place(self, playthrough_name):
        playthrough_manager = PlaythroughManager(playthrough_name)
        llm_client = OpenRouterLlmClientFactory().create_llm_client()
        strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, self._config_manager.get_heavy_llm()
        )

        character_information_factory = CharacterInformationProvider(
            playthrough_name, playthrough_manager.get_player_identifier()
        )

        description_product = ConcreteFilteredPlaceDescriptionGenerationFactory(
            playthrough_name,
            playthrough_manager.get_player_identifier(),
            playthrough_manager.get_current_place_identifier(),
            strategy_factory,
            character_information_factory,
        ).generate_product()

        if description_product.is_valid():
            description = description_product.get()
        else:
            return description_product.get_error(), None

        # Generate the audio file for the description
        voice_line_file_name = self._generate_place_description_voice_line(
            playthrough_name, description
        )

        return description, voice_line_file_name

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

    @staticmethod
    def generate_world(world_notion: str):
        filesystem_manager = FilesystemManager()

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, ConfigManager().get_heavy_llm()
        )

        world_generation_strategy = WorldGenerationStrategy(
            world_notion,
            produce_tool_response_strategy_factory,
            filesystem_manager=filesystem_manager,
        )

        world_generation_strategy.generate_place()

    @staticmethod
    def generate_region(world_name, region_notion=""):
        strategy = FatheredPlaceGenerationStrategy(
            TemplateType.REGION, world_name, region_notion
        )
        strategy.generate_place()

    @staticmethod
    def generate_area(region_name, area_notion=""):
        strategy = FatheredPlaceGenerationStrategy(
            TemplateType.AREA, region_name, area_notion
        )
        strategy.generate_place()

    @staticmethod
    def generate_location(area_name, location_notion=""):
        strategy = FatheredPlaceGenerationStrategy(
            TemplateType.LOCATION, area_name, location_notion
        )
        strategy.generate_place()

    def _create_visit_place_command_factory(self, playthrough_name):
        strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            self._config_manager.get_heavy_llm(),
        )

        place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
            playthrough_name
        )

        places_descriptions_factory = PlacesDescriptionsFactory(
            place_descriptions_for_prompt_factory
        )

        return VisitPlaceCommandFactory(
            playthrough_name, strategy_factory, places_descriptions_factory
        )
