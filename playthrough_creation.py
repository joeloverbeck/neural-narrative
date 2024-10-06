import sys

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
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
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


def main():
    try:
        interface_manager = ConsoleInterfaceManager()

        # Ask the user for the name of the playthrough
        playthrough_name = interface_manager.prompt_for_input(
            "Enter the name of your playthrough: "
        )

        # Ask the user for the name of the world template
        world_template = interface_manager.prompt_for_input(
            "Enter the name of the world (from those in the template): "
        )

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

        create_player_character_command = GeneratePlayerCharacterCommand(
            playthrough_name,
            input("Enter your notions for how the player character should be: "),
            generate_character_command_factory,
        )

        visit_place_command_factory = VisitPlaceCommandFactory(
            playthrough_name,
            produce_tool_response_strategy_factory,
        )

        # Call the create_playthrough function
        CreatePlaythroughCommand(
            playthrough_name,
            world_template,
            create_playthrough_metadata_command,
            create_initial_map_command,
            create_player_character_command,
            visit_place_command_factory,
        ).execute()

    except Exception as e:
        # Print the exception message and exit the program
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
