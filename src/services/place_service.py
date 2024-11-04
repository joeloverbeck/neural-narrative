from typing import Optional

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.maps.abstracts.factory_products import (
    CardinalConnectionCreationProduct,
)
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.composers.get_current_weather_identifier_algorithm_composer import (
    GetCurrentWeatherIdentifierAlgorithmComposer,
)
from src.maps.composers.random_template_type_map_entry_provider_factory_composer import (
    RandomTemplateTypeMapEntryProviderFactoryComposer,
)
from src.maps.composers.visit_place_command_factory_composer import (
    VisitPlaceCommandFactoryComposer,
)
from src.maps.configs.cardinal_connection_creation_factory_config import (
    CardinalConnectionCreationFactoryConfig,
)
from src.maps.configs.cardinal_connection_creation_factory_factories_config import (
    CardinalConnectionCreationFactoryFactoriesConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_config import (
    FilteredPlaceDescriptionGenerationFactoryConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_factories_config import (
    FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
)
from src.maps.enums import CardinalDirection
from src.maps.factories.concrete_cardinal_connection_creation_factory import (
    ConcreteCardinalConnectionCreationFactory,
)
from src.maps.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.map_repository import MapRepository
from src.maps.models.place_description import PlaceDescription
from src.maps.weathers_manager import WeathersManager
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class PlaceService:

    def __init__(self, llms: Optional[Llms] = None):
        self._llms = llms or Llms()

    @staticmethod
    def _generate_place_description_voice_line(playthrough_name, description_text):
        player = Character(
            playthrough_name,
            PlaythroughManager(playthrough_name).get_player_identifier(),
        )
        return DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            player.name, description_text, player.voice_model
        ).direct_voice_line_generation()

    def run_generate_place_command(
        self, father_place_name: str, template_type: TemplateType, notion: str
    ):
        father_template_type = PARENT_TEMPLATE_TYPE.get(template_type)

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                self._llms.for_place_generation(),
            ).compose_factory()
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
        GeneratePlaceCommand(
            template_type,
            father_template_type,
            father_place_name,
            place_generation_tool_response_provider,
            store_generated_place_command_factory,
        ).execute()

    def describe_place(self, playthrough_name: str):
        playthrough_manager = PlaythroughManager(playthrough_name)
        character_information_factory = CharacterInformationProvider(
            playthrough_name, playthrough_manager.get_player_identifier()
        )
        config = FilteredPlaceDescriptionGenerationFactoryConfig(
            playthrough_name, playthrough_manager.get_current_place_identifier()
        )

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                self._llms.for_place_description(),
            ).compose_factory()
        )
        place_manager_factory = PlaceManagerFactory(playthrough_name)
        map_manager_factory = MapManagerFactory(playthrough_name)
        weathers_manager = WeathersManager()
        factories_config = FilteredPlaceDescriptionGenerationFactoryFactoriesConfig(
            produce_tool_response_strategy_factory,
            character_information_factory,
            place_manager_factory,
            map_manager_factory,
            weathers_manager,
        )

        get_current_weather_identifier_algorithm = (
            GetCurrentWeatherIdentifierAlgorithmComposer(
                playthrough_name
            ).compose_algorithm()
        )

        description_product = ConcreteFilteredPlaceDescriptionGenerationFactory(
            config, factories_config, get_current_weather_identifier_algorithm
        ).generate_product(PlaceDescription)

        if description_product.is_valid():
            description = description_product.get()
        else:
            return description_product.get_error(), None

        voice_line_file_name = self._generate_place_description_voice_line(
            playthrough_name, description
        )
        return description, voice_line_file_name

    @staticmethod
    def create_cardinal_connection(
        playthrough_name: str, cardinal_direction: CardinalDirection
    ) -> CardinalConnectionCreationProduct:
        validate_non_empty_string(playthrough_name, "playthrough_name")

        random_template_type_map_entry_provider_factory = (
            RandomTemplateTypeMapEntryProviderFactoryComposer(
                playthrough_name
            ).compose_factory()
        )

        hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)
        map_manager_factory = MapManagerFactory(playthrough_name)
        map_repository = MapRepository(playthrough_name)
        navigation_manager_factory = NavigationManagerFactory(map_repository)

        return ConcreteCardinalConnectionCreationFactory(
            CardinalConnectionCreationFactoryConfig(
                playthrough_name, cardinal_direction
            ),
            CardinalConnectionCreationFactoryFactoriesConfig(
                random_template_type_map_entry_provider_factory,
                hierarchy_manager_factory,
                map_manager_factory,
                navigation_manager_factory,
            ),
        ).create_cardinal_connection()

    @staticmethod
    def visit_place(playthrough_name: str, place_identifier: str):
        visit_command_factory = VisitPlaceCommandFactoryComposer(
            playthrough_name
        ).compose_factory()

        visit_command_factory.create_visit_place_command(place_identifier).execute()
