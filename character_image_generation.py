from src.images.commands.generate_character_image_command import GenerateCharacterImageCommand
from src.images.factories.openai_generated_image_factory import OpenAIGeneratedImageFactory
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


def main():
    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input("Enter your playthrough name: ")

    GenerateCharacterImageCommand(playthrough_name,
                                  interface_manager.prompt_for_input("Enter the character identifier: "),
                                  OpenAIGeneratedImageFactory(OpenAILlmClientFactory().create_llm_client()),
                                  ConcreteUrlContentFactory()).execute()


if __name__ == "__main__":
    main()
