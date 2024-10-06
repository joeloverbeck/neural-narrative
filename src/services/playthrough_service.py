from src.characters.commands.generate_player_character_command import (
    GeneratePlayerCharacterCommand,
)
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.commands.create_playthrough_command import CreatePlaythroughCommand
from src.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.config.config_manager import ConfigManager
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


class PlaythroughService:

    @staticmethod
    def create_playthrough(
        playthrough_name: str, world_template: str, player_notion: str
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not world_template:
            raise ValueError("world_template can't be empty.")

        # Instantiate necessary commands and factories
        create_playthrough_metadata_command = CreatePlaythroughMetadataCommand(
            playthrough_name, world_template
        )
        create_initial_map_command = CreateInitialMapCommand(
            playthrough_name,
            world_template,
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(playthrough_name),
        )

        llm_client = OpenRouterLlmClientFactory().create_llm_client()
        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, ConfigManager().get_heavy_llm()
        )

        store_generate_character_command_factory = (
            StoreGeneratedCharacterCommandFactory(playthrough_name)
        )

        generated_image_factory = OpenAIGeneratedImageFactory(
            OpenAILlmClientFactory().create_llm_client()
        )

        url_content_factory = ConcreteUrlContentFactory()

        character_description_provider_factory = CharacterDescriptionProviderFactory(
            produce_tool_response_strategy_factory
        )

        generate_character_image_command_factory = GenerateCharacterImageCommandFactory(
            playthrough_name,
            character_description_provider_factory,
            generated_image_factory,
            url_content_factory,
        )

        generate_character_command_factory = GenerateCharacterCommandFactory(
            playthrough_name,
            produce_tool_response_strategy_factory,
            store_generate_character_command_factory,
            generate_character_image_command_factory,
        )

        generate_player_character_command = GeneratePlayerCharacterCommand(
            playthrough_name,
            player_notion,
            generate_character_command_factory,
        )

        visit_place_command_factory = VisitPlaceCommandFactory(
            playthrough_name,
            produce_tool_response_strategy_factory,
        )

        CreatePlaythroughCommand(
            playthrough_name,
            world_template,
            create_playthrough_metadata_command,
            create_initial_map_command,
            generate_player_character_command,
            visit_place_command_factory,
        ).execute()
