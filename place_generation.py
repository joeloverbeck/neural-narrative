import sys

from src.constants import HERMES_405B
from src.enums import TemplateType
from src.maps.strategies.fathered_place_generation_strategy import FatheredPlaceGenerationStrategy
from src.maps.strategies.world_generation_strategy import WorldGenerationStrategy
from src.prompting.factories.open_ai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.prompting import prompt_for_input
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy


def main():
    chosen_place_type = prompt_for_input("What type of place do you want to generate? (world|region|area|location): ")

    try:
        place_template_type = TemplateType(chosen_place_type)
    except ValueError as error:
        print(f"Couldn't create a TemplateType from the chosen place type '{chosen_place_type}'.")
        sys.exit()

    if place_template_type == TemplateType.WORLD:
        WorldGenerationStrategy(
            ConcreteProduceToolResponseStrategy(OpenAILlmClientFactory().create_llm_client(),
                                                model=HERMES_405B)).generate_place()
    else:
        FatheredPlaceGenerationStrategy(place_template_type).generate_place()


if __name__ == "__main__":
    main()
