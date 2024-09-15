import sys

from src.constants import HERMES_405B
from src.enums import TemplateType
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.maps.strategies.fathered_place_generation_strategy import FatheredPlaceGenerationStrategy
from src.maps.strategies.world_generation_strategy import WorldGenerationStrategy
from src.prompting.factories.llm_content_provider_factory import LlmContentProviderFactory
from src.prompting.factories.openrouter_llm_client_factory import OpenRouterLlmClientFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy


def main():
    chosen_place_type = ConsoleInterfaceManager().prompt_for_input(
        "What type of place do you want to generate? (world|region|area|location): ")

    try:
        place_template_type = TemplateType(chosen_place_type)
    except ValueError as error:
        print(f"Couldn't create a TemplateType from the chosen place type '{chosen_place_type}'.")
        sys.exit()

    llm_client = OpenRouterLlmClientFactory().create_llm_client()

    llm_content_provider_factory = LlmContentProviderFactory(llm_client, model=HERMES_405B)

    tool_response_parsing_provider_factory = ToolResponseParsingProviderFactory()

    produce_tool_response_strategy = ConcreteProduceToolResponseStrategy(llm_content_provider_factory,
                                                                         tool_response_parsing_provider_factory)

    if place_template_type == TemplateType.WORLD:
        WorldGenerationStrategy(produce_tool_response_strategy).generate_place()
    else:
        FatheredPlaceGenerationStrategy(place_template_type).generate_place()


if __name__ == "__main__":
    main()
