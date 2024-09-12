from src.abstracts.command import Command
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager


class PrintPlaceTemplateListCommand(Command):
    def __init__(self, template_type: TemplateType):
        assert template_type

        self._template_type = template_type

    def execute(self) -> None:
        filesystem_manager = FilesystemManager()

        templates_file: dict

        if self._template_type == TemplateType.WORLD:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_worlds_template_file())
        elif self._template_type == TemplateType.REGION:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_regions_template_file())
        elif self._template_type == TemplateType.AREA:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_areas_template_file())
        elif self._template_type == TemplateType.LOCATION:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_locations_template_file())
        else:
            raise ValueError(f"This command isn't programmed to handle the template type '{self._template_type}'.")

        # Iterate over the dictionary and print the key and a snippet of the description
        for key, value in templates_file.items():
            description_snippet = value['description'][:100]  # Taking first 100 characters as a snippet
            print(f"Name of {self._template_type.value}: {key}")
            print(f"Description: {description_snippet}...")
            print("-" * 40)
