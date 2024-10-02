import logging
import logging.config
import sys

from src.config.config_manager import ConfigManager
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.maps.strategies.fathered_place_generation_strategy import (
    FatheredPlaceGenerationStrategy,
)
from src.maps.strategies.world_generation_strategy import WorldGenerationStrategy
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


def main():
    logging.config.dictConfig(FilesystemManager().get_logging_config_file())

    chosen_place_type = ConsoleInterfaceManager().prompt_for_input(
        "What type of place do you want to generate? (world|region|area|location): "
    )

    try:
        place_template_type = TemplateType(chosen_place_type)
    except ValueError as error:
        print(
            f"Couldn't create a TemplateType from the chosen place type '{chosen_place_type}'."
        )
        sys.exit()

    llm_client = OpenRouterLlmClientFactory().create_llm_client()

    if place_template_type == TemplateType.WORLD:
        WorldGenerationStrategy(
            ProduceToolResponseStrategyFactory(
                llm_client, ConfigManager().get_heavy_llm()
            )
        ).generate_place()
    else:
        FatheredPlaceGenerationStrategy(place_template_type).generate_place()


if __name__ == "__main__":
    main()
