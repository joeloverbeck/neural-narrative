from typing import Optional

from src.abstracts.command import Command
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager


class StoreGeneratedPlaceCommand(Command):
    def __init__(
        self,
        place_data: dict,
        template_type: TemplateType,
        filesystem_manager: FilesystemManager = None,
    ):
        assert place_data
        assert template_type

        self._place_data = place_data
        self._template_type = template_type

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        # Have to load the corresponding place templates file
        current_places_template_file: Optional[dict]

        file_path: Optional[str]

        if self._template_type == TemplateType.WORLD:
            file_path = self._filesystem_manager.get_file_path_to_worlds_template_file()
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.REGION:
            file_path = (
                self._filesystem_manager.get_file_path_to_regions_template_file()
            )
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.AREA:
            file_path = self._filesystem_manager.get_file_path_to_areas_template_file()
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        elif self._template_type == TemplateType.LOCATION:
            file_path = (
                self._filesystem_manager.get_file_path_to_locations_template_file()
            )
            current_places_template_file = (
                self._filesystem_manager.load_existing_or_new_json_file(file_path)
            )
        else:
            raise ValueError(
                f"Wasn't programmed to load the templates file of template '{self._template_type}'."
            )

        # Make the categories lowercase
        current_places_template_file.update(
            {
                self._place_data["name"]: {
                    "description": self._place_data["description"],
                    "categories": [
                        category.lower() for category in self._place_data["categories"]
                    ],
                }
            }
        )

        self._filesystem_manager.save_json_file(current_places_template_file, file_path)

        print(
            f"Saved {self._template_type.value} template '{self._place_data["name"]}'."
        )
