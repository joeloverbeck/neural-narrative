import logging
import random
from typing import List, Dict, Optional

from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.playthrough_manager import PlaythroughManager

logger = logging.getLogger(__name__)


class MapManager:
    def __init__(
        self,
        playthrough_name: str,
        filesystem_manager: Optional[FilesystemManager] = None,
        identifiers_manager: Optional[IdentifiersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def _load_map_file(self) -> Dict:
        """Load the map file."""
        return self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )

    def _save_map_file(self, map_file: Dict):
        """Save the map file."""
        self._filesystem_manager.save_json_file(
            map_file,
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name),
        )

    def _load_template_file(self, place_type: PlaceType) -> Dict:
        """Load the template file based on place type."""
        file_path_getter = {
            PlaceType.WORLD: self._filesystem_manager.get_file_path_to_worlds_template_file,
            PlaceType.REGION: self._filesystem_manager.get_file_path_to_regions_template_file,
            PlaceType.AREA: self._filesystem_manager.get_file_path_to_areas_template_file,
            PlaceType.LOCATION: self._filesystem_manager.get_file_path_to_locations_template_file,
        }.get(place_type)

        if not file_path_getter:
            raise ValueError(
                f"Template file for place type '{place_type.value}' not found."
            )

        return self._filesystem_manager.load_existing_or_new_json_file(
            file_path_getter()
        )

    @staticmethod
    def _get_place(place_identifier: str, map_file: Dict) -> Dict:
        """Retrieve place data with error handling."""
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID '{place_identifier}' not found.")
        return place

    @staticmethod
    def _get_place_template(place: Dict) -> str:
        """Get the template of a place."""
        template = place.get("place_template")
        if not template:
            raise ValueError(
                f"Place template not found for place ID '{place.get('id', 'unknown')}'."
            )
        return template

    def _get_place_hierarchy(
        self, place_identifier: str, map_file: Dict
    ) -> Dict[str, Optional[Dict]]:
        """Retrieve the hierarchy (region, area, location) for a given place."""
        hierarchy = {"region": None, "area": None, "location": None}
        current_place_id = place_identifier

        while current_place_id:
            place = self._get_place(current_place_id, map_file)
            place_type = self.determine_place_type(current_place_id)

            if place_type == PlaceType.REGION:
                hierarchy["region"] = place
                break
            elif place_type == PlaceType.AREA:
                hierarchy["area"] = place
                current_place_id = place.get("region")
            elif place_type == PlaceType.LOCATION:
                hierarchy["location"] = place
                current_place_id = place.get("area")
            else:
                raise ValueError(f"Unhandled place type '{place_type.value}'.")

        if not hierarchy["region"]:
            raise ValueError("Region not found in the place hierarchy.")

        return hierarchy

    def is_visited(self, place_identifier: str):
        map_file = self._load_map_file()

        return map_file[place_identifier]["visited"]

    def set_as_visited(self, place_identifier: str):
        map_file = self._load_map_file()

        map_file[place_identifier]["visited"] = True

        self._save_map_file(map_file)

    def remove_character_from_place(
        self, character_identifier_to_remove: str, place_identifier: str
    ):
        map_file = self._load_map_file()
        place = self._get_place(place_identifier, map_file)

        place["characters"] = [
            character_id
            for character_id in place.get("characters", [])
            if character_id != character_identifier_to_remove
        ]

        self._save_map_file(map_file)

    def get_current_place_template(self) -> str:
        map_file = self._load_map_file()
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        place = self._get_place(current_place_id, map_file)

        return self._get_place_template(place)

    def get_current_place_type(self) -> PlaceType:
        map_file = self._load_map_file()
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        place = self._get_place(current_place_id, map_file)

        return PlaceType(place.get("type"))

    def get_place_categories(
        self, place_template: str, place_type: PlaceType
    ) -> List[str]:
        templates = self._load_template_file(place_type)
        place_data = templates.get(place_template)

        if not place_data:
            raise ValueError(
                f"'{place_template}' not found in {place_type.value} templates."
            )

        return place_data.get("categories", [])

    @staticmethod
    def filter_places_by_categories(
        place_templates: Dict, father_place_categories: List[str]
    ) -> Dict:
        """Filter places whose categories match any of the father place's categories."""
        return {
            name: data
            for name, data in place_templates.items()
            if set(data.get("categories", [])) & set(father_place_categories)
        }

    @staticmethod
    def select_random_place(matching_places: Dict) -> str:
        """Select a random place from the matching places."""
        if not matching_places:
            raise ValueError(
                "No matching places found. Consider generating places of the desired type."
            )
        return random.choice(list(matching_places.keys()))

    def get_identifier_and_place_template_of_latest_map_entry(self) -> (str, str):
        map_file = self._load_map_file()
        max_id_str = self._identifiers_manager.get_highest_identifier(map_file)
        place = self._get_place(max_id_str, map_file)
        place_template = self._get_place_template(place)
        return max_id_str, place_template

    def determine_place_type(self, place_identifier: str) -> PlaceType:
        map_file = self._load_map_file()
        place = self._get_place(place_identifier, map_file)
        place_type_str = place.get("type")
        try:
            return PlaceType(place_type_str)
        except ValueError:
            raise ValueError(
                f"Unknown place type '{place_type_str}' for place ID '{place_identifier}'."
            )

    def fill_places_parameter(self, place_identifier: str) -> PlacesTemplatesParameter:
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        map_file = self._load_map_file()

        hierarchy = self._get_place_hierarchy(place_identifier, map_file)

        region_template = self._get_place_template(hierarchy["region"])

        area_template = (
            self._get_place_template(hierarchy["area"])
            if hierarchy["area"]
            else region_template
        )

        location_template = (
            self._get_place_template(hierarchy["location"])
            if hierarchy["location"]
            else None
        )

        return PlacesTemplatesParameter(
            region_template=region_template,
            area_template=area_template,
            location_template=location_template,
        )

    def get_place_full_data(
        self, place_identifier: str
    ) -> Dict[str, Optional[Dict[str, str]]]:
        if not place_identifier:
            raise ValueError("place_identifier should not be empty.")

        map_file = self._load_map_file()

        hierarchy = self._get_place_hierarchy(place_identifier, map_file)

        result = {"region_data": None, "area_data": None, "location_data": None}

        for place_type in ["region", "area", "location"]:

            place = hierarchy.get(place_type)

            if place:
                template_name = self._get_place_template(place)
                templates = self._load_template_file(PlaceType(place_type))
                template_data = templates.get(template_name)
                if not template_data:
                    raise ValueError(
                        f"{place_type.capitalize()} template '{template_name}' not found."
                    )
                result[f"{place_type}_data"] = {
                    "name": template_name,
                    "description": template_data.get("description", ""),
                }

        return result

    def get_locations_in_area(self, area_identifier: str) -> List[Dict[str, str]]:
        """
        Retrieve a list of dictionaries containing the identifier and place_template
        of locations within a given area.

        Args:
            area_identifier (str): The identifier of the area.

        Returns:
            List[Dict[str, str]]: A list of dictionaries with keys 'identifier' and 'place_template'.
        """
        if not area_identifier:
            raise ValueError("area_identifier should not be empty.")

        map_file = self._load_map_file()
        locations = []

        for identifier, data in map_file.items():
            if data.get("area") == area_identifier and data.get("type") == "location":
                location_info = {
                    "identifier": identifier,
                    "place_template": data.get("place_template"),
                }
                locations.append(location_info)

        if not locations:
            logger.warning(f"No locations found in area '{area_identifier}'.")

        return locations
