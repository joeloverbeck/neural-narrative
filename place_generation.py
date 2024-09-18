import sys

from src.constants import HERMES_405B
from src.enums import TemplateType
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
            ProduceToolResponseStrategyFactory(llm_client, HERMES_405B)
        ).generate_place()
    else:
        FatheredPlaceGenerationStrategy(place_template_type).generate_place()


if __name__ == "__main__":
    main()
