import sys
from typing import Optional

from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.strategies import PlaceGenerationStrategy
from src.maps.commands.generate_place_command import GeneratePlaceCommand


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
        filesystem_manager = FilesystemManager()

        father_templates_file: Optional[dict]

        if father_template_type == TemplateType.WORLD:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_worlds_template_file())
        elif father_template_type == TemplateType.REGION:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_regions_template_file())
        elif father_template_type == TemplateType.AREA:
            father_templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_areas_template_file())
        else:
            print(f"This program wasn't made to handle father template type '{father_template_type}'.")
            sys.exit()

        # Iterate over the dictionary and print the key and a snippet of the description
        for key, value in father_templates_file.items():
            description_snippet = value['description'][:100]  # Taking first 100 characters as a snippet
            print(f"Name of {father_template_type.value}: {key}")
            print(f"Description: {description_snippet}...")
            print("-" * 40)

        GeneratePlaceCommand(self._place_template_type, father_template_type).execute()
