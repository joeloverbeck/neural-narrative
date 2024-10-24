from typing import Optional

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
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
from src.maps.models.area import Area
from src.maps.models.location import Location
from src.maps.models.region import Region
from src.maps.models.world import World
from src.maps.weathers_manager import WeathersManager
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.enums import LlmClientType
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

        if template_type == TemplateType.LOCATION:
            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    LlmClientType.INSTRUCTOR,
                    self._llms.for_place_generation(),
                    Location,
                ).compose_factory()
            )
        elif template_type == TemplateType.AREA:
            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    LlmClientType.INSTRUCTOR, self._llms.for_place_generation(), Area
                ).compose_factory()
            )
        elif template_type == TemplateType.REGION:
            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    LlmClientType.INSTRUCTOR, self._llms.for_place_generation(), Region
                ).compose_factory()
            )
        elif template_type == TemplateType.WORLD:
            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    LlmClientType.INSTRUCTOR, self._llms.for_place_generation(), World
                ).compose_factory()
            )
        else:
            raise NotImplemented(
                f"Case not handled for template type '{template_type}'."
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
                LlmClientType.OPEN_ROUTER, self._llms.for_place_description()
            ).compose_factory()
        )
        place_manager_factory = PlaceManagerFactory(playthrough_name)
        map_manager_factory = MapManagerFactory(playthrough_name)
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
        voice_line_file_name = self._generate_place_description_voice_line(
            playthrough_name, description
        )
        return description, voice_line_file_name

    @staticmethod
    def exit_location(playthrough_name: str):
        playthrough_manager = PlaythroughManager(playthrough_name)
        filesystem_manager = FilesystemManager()
        if (
            not PlaceManagerFactory(playthrough_name)
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
            playthrough_name
        ).compose_factory()
        visit_command_factory.create_visit_place_command(destination_area).execute()

    @staticmethod
    def visit_location(playthrough_name: str, location_identifier: str):
        visit_command_factory = VisitPlaceCommandFactoryComposer(
            playthrough_name
        ).compose_factory()
        visit_command_factory.create_visit_place_command(location_identifier).execute()
