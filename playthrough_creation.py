import sys

from src.characters.commands.generate_initial_characters_command import (
    GenerateInitialCharactersCommand,
)
from src.commands.create_playthrough_command import CreatePlaythroughCommand
from src.commands.create_playthrough_metadata_command import (
    CreatePlaythroughMetadataCommand,
)
from src.constants import HERMES_405B
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.maps.commands.create_initial_map_command import CreateInitialMapCommand
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.map_manager import MapManager
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
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
                MapManager(playthrough_name)
            ),
        )

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, HERMES_405B
        )

        create_initial_characters_command = GenerateInitialCharactersCommand(
            playthrough_name,
            produce_tool_response_strategy_factory,
            OpenAIGeneratedImageFactory(OpenAILlmClientFactory().create_llm_client()),
            ConcreteUrlContentFactory(),
        )

        # Call the create_playthrough function
        CreatePlaythroughCommand(
            playthrough_name,
            world_template,
            create_playthrough_metadata_command,
            create_initial_map_command,
            create_initial_characters_command,
        ).execute()

    except Exception as e:
        # Print the exception message and exit the program
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
