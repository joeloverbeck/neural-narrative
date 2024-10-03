from src.config.config_manager import ConfigManager
from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_manager import MapManager
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

        return VisitPlaceCommandFactory(playthrough_name, strategy_factory)
