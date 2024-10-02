import sys

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.factories.automatic_user_content_for_character_generation_factory import (
    AutomaticUserContentForCharacterGenerationFactory,
)
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.player_guided_user_content_for_character_generation_factory import (
    PlayerGuidedUserContentForCharacterGenerationFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


def main():
    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input(
        "Enter your playthrough name: "
    )

    filesystem_manager = FilesystemManager()

    if not filesystem_manager.does_file_path_exist(
        filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name)
    ):
        print(f"There is no playthrough named '{playthrough_name}'")
        sys.exit()

    places_parameter = (
        ConsoleInterfaceManager().create_places_templates_parameter_for_character_generation()
    )

    llm_client = OpenRouterLlmClientFactory().create_llm_client()

    produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
        llm_client, ConfigManager().get_heavy_llm()
    )

    guided_character_generation_tool_response_provider = (
        CharacterGenerationToolResponseProvider(
            playthrough_name,
            places_parameter,
            produce_tool_response_strategy_factory,
            PlayerGuidedUserContentForCharacterGenerationFactory(),
        )
    )

    random_character_generation_tool_response_provider = (
        CharacterGenerationToolResponseProvider(
            playthrough_name,
            places_parameter,
            produce_tool_response_strategy_factory,
            AutomaticUserContentForCharacterGenerationFactory(),
        )
    )

    store_generate_character_command_factory = StoreGeneratedCharacterCommandFactory(
        playthrough_name
    )

    generated_image_factory = OpenAIGeneratedImageFactory(
        OpenAILlmClientFactory().create_llm_client()
    )

    url_content_factory = ConcreteUrlContentFactory()

    generate_character_image_command_factory = GenerateCharacterImageCommandFactory(
        playthrough_name, generated_image_factory, url_content_factory
    )

    if (
        ConsoleInterfaceManager()
        .prompt_for_input("Do you want to guide character creation?: ")
        .lower()
        == "yes"
    ):
        GenerateCharacterCommand(
            playthrough_name,
            guided_character_generation_tool_response_provider,
            store_generate_character_command_factory,
            generate_character_image_command_factory,
            place_character_at_current_place=True,
        ).execute()
        return

    GenerateCharacterCommand(
        playthrough_name,
        random_character_generation_tool_response_provider,
        store_generate_character_command_factory,
        generate_character_image_command_factory,
        place_character_at_current_place=True,
    ).execute()


if __name__ == "__main__":
    main()
