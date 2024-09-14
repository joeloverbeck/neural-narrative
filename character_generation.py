import sys

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.constants import HERMES_405B
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.images.factories.openai_generated_image_factory import OpenAIGeneratedImageFactory
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.maps.commands.print_place_template_list_command import PrintPlaceTemplateListCommand
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.factories.automatic_user_content_for_character_generation_factory import \
    AutomaticUserContentForCharacterGenerationFactory
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import OpenRouterLlmClientFactory
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory


def main():
    interface_manager = ConsoleInterfaceManager()

    playthrough_name = interface_manager.prompt_for_input("Enter your playthrough name: ")

    filesystem_manager = FilesystemManager()

    if not filesystem_manager.does_file_path_exist(
            filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name)):
        print(f"There is no playthrough named '{playthrough_name}'")
        sys.exit()

    PrintPlaceTemplateListCommand(TemplateType.REGION).execute()

    region_template = interface_manager.prompt_for_input("To what region does the character belong?: ")

    PrintPlaceTemplateListCommand(TemplateType.AREA).execute()

    area_template = interface_manager.prompt_for_input("To what area does the character belong?: ")

    PrintPlaceTemplateListCommand(TemplateType.LOCATION).execute()

    location_template = input(
        "To what location does the character belong? (could be empty): ")

    # Now we have to ask for the places involved.
    places_parameter = PlacesTemplatesParameter(region_template, area_template, location_template)

    GenerateCharacterCommand(playthrough_name, places_parameter,
                             ConcreteProduceToolResponseStrategy(OpenRouterLlmClientFactory().create_llm_client(),
                                                                 model=HERMES_405B),
                             AutomaticUserContentForCharacterGenerationFactory(),
                             OpenAIGeneratedImageFactory(OpenAILlmClientFactory().create_llm_client()),
                             ConcreteUrlContentFactory()).execute()


if __name__ == "__main__":
    main()
