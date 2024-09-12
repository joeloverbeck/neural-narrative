from src.characters.commands.store_generated_character_command import StoreGeneratedCharacterCommand
from src.constants import HERMES_405B
from src.prompting.factories.character_generation_tool_response_factory import CharacterGenerationToolResponseFactory
from src.prompting.factories.character_tool_response_data_extraction_factory import \
    CharacterToolResponseDataExtractionFactory
from src.prompting.factories.open_ai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.prompting import prompt_for_input
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy


def main():
    playthrough_name = prompt_for_input("Enter your playthrough name: ")
    user_input = prompt_for_input("What kind of character would you like to generate? ")

    model = HERMES_405B

    llm_tool_response_product = CharacterGenerationToolResponseFactory(playthrough_name, user_input,
                                                                       ConcreteProduceToolResponseStrategy(
                                                                           OpenAILlmClientFactory().create_llm_client(),
                                                                           model)).create_llm_response()

    if llm_tool_response_product.is_valid():
        # Extract character data using the function provided
        character_data = CharacterToolResponseDataExtractionFactory(
            llm_tool_response_product.get()).extract_data().get()

        StoreGeneratedCharacterCommand(playthrough_name, character_data).execute()


if __name__ == "__main__":
    main()
