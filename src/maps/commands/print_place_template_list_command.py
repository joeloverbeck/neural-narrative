from src.base.abstracts.command import Command
from src.base.constants import WORLDS_TEMPLATES_FILE, LOCATIONS_TEMPLATES_FILE, AREAS_TEMPLATES_FILE, \
    REGIONS_TEMPLATES_FILE
from src.base.enums import TemplateType
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
                WORLDS_TEMPLATES_FILE)
        elif self._template_type == TemplateType.REGION:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                REGIONS_TEMPLATES_FILE)
        elif self._template_type == TemplateType.AREA:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                AREAS_TEMPLATES_FILE)
        elif self._template_type == TemplateType.LOCATION:
            templates_file = filesystem_manager.load_existing_or_new_json_file(
                LOCATIONS_TEMPLATES_FILE)
        else:
            raise ValueError(
                f"This command isn't programmed to handle the template type '{self._template_type}'."
            )
        for key, value in templates_file.items():
            if not key:
                raise ValueError('Got a null key.')
            if not value:
                raise ValueError(
                    f'There is no data for key {key} in file:\n{templates_file}'
                )
            if not value['description']:
                raise ValueError(
                    f"""Found a place without a description. It was the key {key} in the file:
{templates_file}"""
                )
            description_snippet = value['description'][:100]
            print(f'Name of {self._template_type}: {key}')
            print(f'Description: {description_snippet}...')
            print('-' * 40)
