from typing import Optional

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import PlaceType, TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.playthrough_name import RequiredString
from src.characters.character import Character
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.maps.map_manager import MapManager
from src.prompting.factories.concrete_filtered_place_description_generation_factory import (
    ConcreteFilteredPlaceDescriptionGenerationFactory,
)
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

    def exit_location(self, playthrough_name: str):
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
            RequiredString(playthrough_name)
        )
        visit_command_factory.create_visit_place_command(destination_area).execute()

    def visit_location(self, playthrough_name, location_identifier):
        visit_command_factory = self._create_visit_place_command_factory(
            RequiredString(playthrough_name)
        )
        visit_command_factory.create_visit_place_command(location_identifier).execute()

    def _create_visit_place_command_factory(self, playthrough_name: RequiredString):
        strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            self._config_manager.get_heavy_llm(),
        )

        place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
            playthrough_name.value
        )

        places_descriptions_factory = PlacesDescriptionsFactory(
            place_descriptions_for_prompt_factory
        )

        return VisitPlaceCommandFactory(
            playthrough_name.value, strategy_factory, places_descriptions_factory
        )
