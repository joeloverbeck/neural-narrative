from typing import Optional

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.composers.visit_place_command_factory_composer import (
    VisitPlaceCommandFactoryComposer,
)
from src.maps.configs.filtered_place_description_generation_factory_config import (
    FilteredPlaceDescriptionGenerationFactoryConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_factories_config import (
    FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
)
from src.maps.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.weathers_manager import WeathersManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class PlaceService:
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
    ):
        self._config_manager = config_manager or ConfigManager()

    @staticmethod
    def _generate_place_description_voice_line(playthrough_name, description_text):
        # Load the player's voice model.
        player = Character(
            playthrough_name,
            PlaythroughManager(playthrough_name).get_player_identifier(),
        )

        return DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            player.name, description_text, player.voice_model
        ).direct_voice_line_generation()

    @staticmethod
    def run_generate_place_command(
        father_place_name: RequiredString,
        template_type: TemplateType,
        notion: RequiredString,
    ):
        father_template_type = PARENT_TEMPLATE_TYPE.get(template_type)

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )

        place_generation_tool_response_provider = PlaceGenerationToolResponseProvider(
            father_place_name,
            template_type,
            notion,
            produce_tool_response_strategy_factory,
        )

        store_generated_place_command_factory = StoreGeneratedPlaceCommandFactory(
            template_type
        )

        # Generate the place using the provided parameters
        GeneratePlaceCommand(
            template_type,
            father_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        ).execute()

    def describe_place(self, playthrough_name: RequiredString):
        playthrough_manager = PlaythroughManager(playthrough_name)

        character_information_factory = CharacterInformationProvider(
            playthrough_name, playthrough_manager.get_player_identifier()
        )

        config = FilteredPlaceDescriptionGenerationFactoryConfig(
            RequiredString(playthrough_name),
            RequiredString(playthrough_manager.get_current_place_identifier()),
        )

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )

        place_manager_factory = PlaceManagerFactory(RequiredString(playthrough_name))

        map_manager_factory = MapManagerFactory(RequiredString(playthrough_name))

        weathers_manager = WeathersManager(map_manager_factory)

        factories_config = FilteredPlaceDescriptionGenerationFactoryFactoriesConfig(
            produce_tool_response_strategy_factory,
            character_information_factory,
            place_manager_factory,
            map_manager_factory,
            weathers_manager,
        )

        description_product = ConcreteFilteredPlaceDescriptionGenerationFactory(
            config, factories_config
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

    @staticmethod
    def exit_location(playthrough_name: RequiredString):
        playthrough_manager = PlaythroughManager(playthrough_name)
        filesystem_manager = FilesystemManager()

        if (
            not PlaceManagerFactory(RequiredString(playthrough_name))
            .create_place_manager()
            .get_current_place_type()
            == TemplateType.LOCATION
        ):
            raise ValueError(
                "Somehow tried to exit a location when the current place wasn't a location."
            )

        map_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_map(playthrough_name)
        )
        current_place_identifier = playthrough_manager.get_current_place_identifier()
        destination_area = map_file[current_place_identifier]["area"]

        visit_command_factory = VisitPlaceCommandFactoryComposer(
            RequiredString(playthrough_name)
        ).compose_factory()
        visit_command_factory.create_visit_place_command(destination_area).execute()

    @staticmethod
    def visit_location(
        playthrough_name: RequiredString, location_identifier: RequiredString
    ):
        visit_command_factory = VisitPlaceCommandFactoryComposer(
            playthrough_name
        ).compose_factory()
        visit_command_factory.create_visit_place_command(location_identifier).execute()
