# src/repositories/places_facts_repository.py
from typing import Dict, Any

from src.base.enums import TemplateType
from src.filesystem.file_operations import (
    read_json_file,
    write_json_file,
    create_empty_json_file_if_not_exists,
)
from src.filesystem.path_manager import PathManager


class PlacesFactsRepository:
    TEMPLATE_TYPE_TO_FACTS_PATH = {
        TemplateType.STORY_UNIVERSE: PathManager.get_story_universes_facts_path,
        TemplateType.WORLD: PathManager.get_worlds_facts_path,
        TemplateType.REGION: PathManager.get_regions_facts_path,
        TemplateType.AREA: PathManager.get_areas_facts_path,
        TemplateType.LOCATION: PathManager.get_locations_facts_path,
        TemplateType.ROOM: PathManager.get_rooms_facts_path,
    }

    @classmethod
    def get_place_facts(
        cls, place_template: str, template_type: TemplateType
    ) -> Dict[str, Any]:
        """
        Retrieves the facts dictionary for the given place_template from the appropriate places_facts file.

        Args:
            place_template (str): The name of the place template.
            template_type (TemplateType): The type of the template.

        Returns:
            Dict[str, Any]: The facts dictionary corresponding to the place_template.
        """
        # Get the path to the facts file
        path_getter = cls.TEMPLATE_TYPE_TO_FACTS_PATH.get(template_type)
        if not path_getter:
            raise ValueError(f"Unknown TemplateType: {template_type}")

        facts_file_path = path_getter()

        create_empty_json_file_if_not_exists(facts_file_path)

        data = read_json_file(facts_file_path)

        # Return the facts for the given place_template
        return data.get(place_template, {})

    @classmethod
    def set_place_facts(
        cls, place_template: str, data: Dict[str, Any], template_type: TemplateType
    ) -> None:
        """
        Sets the facts for the given place_template in the appropriate places_facts file.

        Args:
            place_template (str): The name of the place template.
            data (Dict[str, Any]): The facts data to set.
            template_type (TemplateType): The type of the template.
        """
        # Get the path to the facts file
        path_getter = cls.TEMPLATE_TYPE_TO_FACTS_PATH.get(template_type)
        if not path_getter:
            raise ValueError(f"Unknown TemplateType: {template_type}")

        facts_file_path = path_getter()

        # Read existing data or create a new dictionary if the file doesn't exist
        if facts_file_path.exists():
            all_data = read_json_file(facts_file_path)
        else:
            all_data = {}

        # Update the data
        all_data[place_template] = data

        # Write back to the file
        write_json_file(facts_file_path, all_data)
