from typing import List, Optional
from src.base.enums import TemplateType
from src.maps.commands.print_place_template_list_command import PrintPlaceTemplateListCommand
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class ConsoleInterfaceManager:

    def prompt_for_character_identifier(self, prompt_text: str) -> Optional[str
    ]:
        """Prompt user for a character identifier, allow empty input."""
        user_input = input(prompt_text)
        if user_input.strip() == '':
            return None
        try:
            character_identifier = int(user_input)
        except ValueError:
            print('Invalid input. Please enter a valid integer.')
            return self.prompt_for_character_identifier(prompt_text)
        return str(character_identifier)

    @staticmethod
    def prompt_for_multiple_identifiers(prompt_text: str) -> List[str]:
        """Prompt for multiple character identifiers."""
        while True:
            user_input = input(prompt_text)
            if user_input.strip() == '':
                return []
            identifiers = [x.strip() for x in user_input.replace(',', ' ').
            split() if x.strip()]
            return identifiers

    @staticmethod
    def prompt_for_input(prompt_text: str) -> str:
        """Prompt user for input until valid data is provided."""
        while True:
            user_input = input(prompt_text)
            if user_input:
                return user_input
            else:
                print(f'{prompt_text} cannot be empty. Please try again.')

    def create_places_templates_parameter_for_character_generation(self
                                                                   ) -> PlacesTemplatesParameter:
        PrintPlaceTemplateListCommand(TemplateType.WORLD).execute()
        world_template = self.prompt_for_input(
            'To what world does the character belong?: ')
        PrintPlaceTemplateListCommand(TemplateType.REGION).execute()
        region_template = self.prompt_for_input(
            'To what region does the character belong?: ')
        PrintPlaceTemplateListCommand(TemplateType.AREA).execute()
        area_template = self.prompt_for_input(
            'To what area does the character belong?: ')
        PrintPlaceTemplateListCommand(TemplateType.LOCATION).execute()
        location_template = input(
            'To what location does the character belong? (could be empty): ')
        return PlacesTemplatesParameter(world_template, region_template,
                                        area_template, location_template)
