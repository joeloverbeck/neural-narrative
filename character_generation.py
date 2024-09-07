from openai import OpenAI

from src.characters.commands.store_generated_character_command import StoreGeneratedCharacterCommand
from src.constants import OPENROUTER_API_URL
from src.files import load_secret_key
from src.prompting.factories.character_generation_tool_response_factory import CharacterGenerationToolResponseFactory
from src.prompting.factories.character_tool_response_data_extraction_factory import \
    CharacterToolResponseDataExtractionFactory
from src.prompting.prompting import prompt_for_input


def main():
    playthrough_name = prompt_for_input("Enter your playthrough name: ")
    user_input = prompt_for_input("What kind of character would you like to generate? ")

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
        base_url=OPENROUTER_API_URL,
        api_key=load_secret_key(),
    )

    llm_tool_response_product = CharacterGenerationToolResponseFactory(client,
                                                                       user_input).create_llm_response()

    if llm_tool_response_product.is_valid():
        # Extract character data using the function provided
        character_data = CharacterToolResponseDataExtractionFactory(
            llm_tool_response_product.get()).extract_data().get()

        StoreGeneratedCharacterCommand(playthrough_name, character_data).execute()


if __name__ == "__main__":
    main()
