import sys

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.constants import HERMES_405B
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.commands.print_place_template_list_command import PrintPlaceTemplateListCommand
from src.maps.places_parameter import PlacesParameter
from src.prompting.factories.open_ai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.prompting import prompt_for_input
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy


def main():
    playthrough_name = prompt_for_input("Enter your playthrough name: ")

    filesystem_manager = FilesystemManager()

    if not filesystem_manager.does_file_path_exist(
            filesystem_manager.get_file_path_to_playthrough_folder(playthrough_name)):
        print(f"There is no playthrough named '{playthrough_name}'")
        sys.exit()

    PrintPlaceTemplateListCommand(TemplateType.REGION).execute()

    region_template = prompt_for_input("To what region does the character belong?: ")

    PrintPlaceTemplateListCommand(TemplateType.AREA).execute()

    area_template = prompt_for_input("To what area does the character belong?: ")

    PrintPlaceTemplateListCommand(TemplateType.LOCATION).execute()

    location_template = input(
        "To what location does the character belong? (could be empty): ")

    # Now we have to ask for the places involved.
    places_parameter = PlacesParameter(region_template, area_template, location_template)

    GenerateCharacterCommand(playthrough_name, places_parameter,
                             ConcreteProduceToolResponseStrategy(OpenAILlmClientFactory().create_llm_client(),
                                                                 model=HERMES_405B)).execute()


if __name__ == "__main__":
    main()
