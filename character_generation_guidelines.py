import sys

from src.characters.commands.generate_character_generation_guidelines_command import (
    GenerateCharacterGenerationGuidelinesCommand,
)
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
)
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


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

    place_identifier = str(
        interface_manager.prompt_for_input(
            "Enter the place identifier of your map for which you want to create the guidelines: "
        )
    )

    produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
        OpenRouterLlmClientFactory().create_llm_client(),
        ConfigManager().get_heavy_llm(),
    )

    character_generation_guidelines_factory = CharacterGenerationGuidelinesFactory(
        playthrough_name, place_identifier, produce_tool_response_strategy_factory
    )

    GenerateCharacterGenerationGuidelinesCommand(
        playthrough_name, place_identifier, character_generation_guidelines_factory
    ).execute()


if __name__ == "__main__":
    main()
