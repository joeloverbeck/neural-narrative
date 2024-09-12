import sys
from typing import Optional

from src.enums import TemplateType
from src.maps.abstracts.strategies import PlaceGenerationStrategy
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.commands.print_place_template_list_command import PrintPlaceTemplateListCommand


class FatheredPlaceGenerationStrategy(PlaceGenerationStrategy):
    def __init__(self, place_template_type: TemplateType):
        assert place_template_type

        self._place_template_type = place_template_type

    def generate_place(self):
        father_template_type: Optional[TemplateType]

        if self._place_template_type == TemplateType.REGION:
            father_template_type = TemplateType.WORLD
        elif self._place_template_type == TemplateType.AREA:
            father_template_type = TemplateType.REGION
        elif self._place_template_type == TemplateType.LOCATION:
            father_template_type = TemplateType.AREA
        else:
            print(f"This program isn't made to generate the place type '{self._place_template_type}'.")
            sys.exit()

        # May as well write on the console the names and some description of the place, so the user
        # can choose them without having to mess with the files.
        PrintPlaceTemplateListCommand(father_template_type).execute()

        GeneratePlaceCommand(self._place_template_type, father_template_type).execute()
