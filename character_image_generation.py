from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.config.config_manager import ConfigManager
from src.images.commands.generate_character_image_command import (
    GenerateCharacterImageCommand,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


def main():
    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input(
        "Enter your playthrough name: "
    )

    produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
        OpenRouterLlmClientFactory().create_llm_client(),
        ConfigManager().get_heavy_llm(),
    )

    character_description_provider_factory = CharacterDescriptionProviderFactory(
        produce_tool_response_strategy_factory
    )

    GenerateCharacterImageCommand(
        playthrough_name,
        interface_manager.prompt_for_input("Enter the character identifier: "),
        character_description_provider_factory,
        OpenAIGeneratedImageFactory(OpenAILlmClientFactory().create_llm_client()),
        ConcreteUrlContentFactory(),
    ).execute()


if __name__ == "__main__":
    main()
