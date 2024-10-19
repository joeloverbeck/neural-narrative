import logging
import random
from typing import List, Dict, Optional

from src.base.constants import (
    WORLDS_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
)
from src.base.enums import PlaceType
from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.enums import CardinalDirection
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.maps.weather_identifier import WeatherIdentifier

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
        file_path = {
            PlaceType.WORLD: WORLDS_TEMPLATES_FILE,
            PlaceType.REGION: REGIONS_TEMPLATES_FILE,
            PlaceType.AREA: AREAS_TEMPLATES_FILE,
            PlaceType.LOCATION: LOCATIONS_TEMPLATES_FILE,
        }.get(place_type)

        if not file_path:
            raise ValueError(
                f"Template file for place type '{place_type.value}' not found."
            )

        return self._filesystem_manager.load_existing_or_new_json_file(file_path)

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

    def get_available_location_types(self):
        # Get the categories of the current area
        place_categories = self.get_place_categories(
            self.get_current_place_template(), PlaceType.AREA
        )

        # Load location templates
        location_templates = self._load_template_file(PlaceType.LOCATION)

        # Filter locations based on categories
        filtered_places = self.filter_places_by_categories(
            location_templates, place_categories
        )

        # Get the list of used place templates to avoid duplicates
        used_place_templates = self.get_place_templates_of_type(PlaceType.LOCATION)

        # Further filter out places whose template has already been used
        available_places = {
            identifier: data
            for identifier, data in filtered_places.items()
            if identifier not in used_place_templates
        }

        # Extract unique types from the filtered places
        return list(
            set(
                data.get("type")
                for data in available_places.values()
                if data.get("type")
            )
        )

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

    def get_current_area(self) -> dict:
        # The current place may already be an area.
        map_file = self._load_map_file()

        if self.get_current_place_type() == PlaceType.AREA:
            return map_file[self._playthrough_manager.get_current_place_identifier()]

        # At this point, the current place type must be an area.
        if not self.get_current_place_type() == PlaceType.LOCATION:
            raise ValueError(
                f"At this point, wasn't expecting the current location to be {self.get_current_place_type()}"
            )

        current_area_identifier = map_file[
            self._playthrough_manager.get_current_place_identifier()
        ]["area"]

        return map_file[current_area_identifier]

    def get_world_description(self):
        worlds_templates_file = self._filesystem_manager.load_existing_or_new_json_file(
            WORLDS_TEMPLATES_FILE
        )

        return worlds_templates_file[self._playthrough_manager.get_world_template()][
            "description"
        ]

    def get_place_description(self, place_identifier: str) -> str:
        """
        Retrieve the description of a place given its identifier, regardless of its type.

        Args:
            place_identifier (str): The identifier of the place.

        Returns:
            str: The description of the place.

        Raises:
            ValueError: If the place identifier is invalid, or if the description is not found.
        """
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        map_file = self._load_map_file()
        place = self._get_place(place_identifier, map_file)
        place_template = self._get_place_template(place)
        place_type = self.determine_place_type(place_identifier)
        templates = self._load_template_file(place_type)
        template_data = templates.get(place_template)

        if not template_data:
            raise ValueError(
                f"Template '{place_template}' not found in {place_type.value} templates."
            )

        description = template_data.get("description")
        if not description:
            raise ValueError(f"No description found in template '{place_template}'.")

        return description

    def get_father_identifier(self, place_identifier: str) -> str:
        """
        Retrieve the father identifier of a given place identifier.
        For areas, this will be the 'region' it belongs to.
        For locations, this will be the 'area' it belongs to.

        Args:
            place_identifier (str): The identifier of the place.

        Returns:
            str: The father identifier of the given place.

        Raises:
            ValueError: If the place_identifier is empty or invalid,
                        or if the place is a region (which has no father),
                        or if the place type is unhandled.
        """
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        map_file = self._load_map_file()
        place = self._get_place(place_identifier, map_file)
        place_type = self.determine_place_type(place_identifier)

        if place_type == PlaceType.AREA:
            father_identifier = place.get("region")
            if not father_identifier:
                raise ValueError(f"Area '{place_identifier}' has no 'region' key.")
            return father_identifier
        elif place_type == PlaceType.LOCATION:
            father_identifier = place.get("area")
            if not father_identifier:
                raise ValueError(f"Location '{place_identifier}' has no 'area' key.")
            return father_identifier
        elif place_type == PlaceType.REGION:
            raise ValueError(f"Region '{place_identifier}' has no father identifier.")
        else:
            raise ValueError(
                f"Unhandled place type '{place_type.value}' for identifier '{place_identifier}'."
            )

    def get_father_template(self) -> str:
        current_place_id = self._playthrough_manager.get_current_place_identifier()

        places_parameter = self.fill_places_templates_parameter(current_place_id)

        current_place_type = self.get_current_place_type()

        if current_place_type == PlaceType.LOCATION:
            return places_parameter.get_area_template()
        if current_place_type == PlaceType.AREA:
            return places_parameter.get_region_template()

        raise ValueError(
            f"This function isn't prepared to handle the place type '{current_place_type.value}'."
        )

    def get_current_place_type(self) -> PlaceType:
        map_file = self._load_map_file()
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        place = self._get_place(current_place_id, map_file)

        return PlaceType(place.get("type"))

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
        place_templates: Dict,
        father_place_categories: List[str],
        location_type: str = None,
    ) -> Dict:
        """Filter places whose categories match any of the father place's categories."""
        filtered_places = {}

        for name, data in place_templates.items():
            place_categories = data.get("categories", [])
            place_type = data.get("type", None)

            # Match categories
            if not any(
                category in place_categories for category in father_place_categories
            ):
                continue

            # If location_type is specified, check if it matches
            if location_type and place_type != location_type:
                continue

            filtered_places[name] = data

        return filtered_places

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

    def fill_places_templates_parameter(
        self, place_identifier: str
    ) -> PlacesTemplatesParameter:
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

                result_data: Dict[str, str] = {
                    "name": template_name,
                    "description": template_data.get("description", ""),
                }

                result[f"{place_type}_data"] = result_data

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

    def get_place_templates_of_type(self, place_type: PlaceType) -> List[str]:
        """
        Retrieve a list of place templates for places of the specified type in the map file.

        Args:
            place_type (PlaceType): The type of places to retrieve templates for.

        Returns:
            List[str]: A list of place template names.
        """
        map_file = self._load_map_file()

        return [
            place_data.get("place_template")
            for place_data in map_file.values()
            if place_data.get("type") == place_type.value
        ]

    def does_area_have_cardinal_connection(
        self, area_identifier: str, cardinal_direction: CardinalDirection
    ):
        if not area_identifier:
            raise ValueError("area_identifier can't be empty.")

        map_file = self._load_map_file()

        # Let's ensure that the place is an area.
        if not map_file[area_identifier]["type"] == PlaceType.AREA.value:
            raise ValueError(
                f"The given identifier '{area_identifier}' didn't belong to an area, but to a '{map_file[area_identifier]["type"]}'."
            )

        area_entry = map_file[area_identifier]

        return cardinal_direction.value in area_entry

    def get_cardinal_connections(
        self, area_identifier: str
    ) -> Dict[str, Optional[Dict[str, str]]]:
        """
        Retrieve the cardinal connections for a given area.

        Args:
            area_identifier (str): The identifier of the area.

        Returns:
            Dict[str, Optional[Dict[str, str]]]: A dictionary with keys as cardinal directions
            ('north', 'south', 'east', 'west') and values as dictionaries containing 'identifier' and 'place_template'
            of the connected areas, or None if there is no connection in that direction.
        """
        if not area_identifier:
            raise ValueError("area_identifier can't be empty.")

        map_file = self._load_map_file()

        if area_identifier not in map_file:
            raise ValueError(f"Area identifier '{area_identifier}' not found in map.")

        area_entry = map_file[area_identifier]

        # Ensure the place is an area
        if area_entry.get("type") != PlaceType.AREA.value:
            raise ValueError(
                f"The given identifier '{area_identifier}' is not an area, but a '{area_entry.get('type')}'."
            )

        result = {}

        # Iterate over all cardinal directions
        for direction in [d.value for d in CardinalDirection]:
            connected_area_id = area_entry.get(direction)

            if connected_area_id:
                connected_area = map_file.get(connected_area_id)
                if not connected_area:
                    logger.warning(
                        f"Connected area '{connected_area_id}' not found in map."
                    )
                    result[direction] = None
                else:
                    place_template = connected_area.get("place_template")
                    if not place_template:
                        logger.warning(
                            f"Place template not found for connected area '{connected_area_id}'."
                        )
                        place_template = None
                    result[direction] = {
                        "identifier": connected_area_id,
                        "place_template": place_template,
                    }
            else:
                result[direction] = None

        return result

    def create_cardinal_connection(
        self,
        cardinal_direction: CardinalDirection,
        origin_identifier: str,
        destination_identifier: str,
    ):
        if not origin_identifier:
            raise ValueError("origin_identifier can't be empty.")
        if not destination_identifier:
            raise ValueError("destination_identifier can't be empty.")

        map_data = self._load_map_file()

        if cardinal_direction.value in map_data[origin_identifier]:
            raise ValueError(
                f"There was already a cardinal connection for '{cardinal_direction.value}' in '{origin_identifier}'."
            )

        map_data[origin_identifier][cardinal_direction.value] = destination_identifier

        self._save_map_file(map_data)

    @staticmethod
    def get_opposite_cardinal_direction(
        cardinal_direction: CardinalDirection,
    ) -> CardinalDirection:
        if cardinal_direction == CardinalDirection.NORTH:
            return CardinalDirection.SOUTH
        elif cardinal_direction == CardinalDirection.SOUTH:
            return CardinalDirection.NORTH
        elif cardinal_direction == CardinalDirection.EAST:
            return CardinalDirection.WEST
        elif cardinal_direction == CardinalDirection.WEST:
            return CardinalDirection.EAST
        else:
            raise ValueError(
                f"Case not handled for cardinal direction '{cardinal_direction}'"
            )

    def add_location(self, place_identifier: str):
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        if not self.get_current_place_type() == PlaceType.AREA:
            raise ValueError(
                "Attempted to add a location to a place that wasn't an area."
            )

        map_file = self._load_map_file()

        # If it turns out that the place_identifier about to be added is already one of the locations,
        # something has gone wrong up to this point.
        if (
            place_identifier
            in map_file[self._playthrough_manager.get_current_place_identifier()][
                "locations"
            ]
        ):
            raise ValueError(
                f"Place identifier '{place_identifier}' already present in the locations of the current area."
            )

        map_file[self._playthrough_manager.get_current_place_identifier()][
            "locations"
        ].append(place_identifier)

        self._save_map_file(map_file)

    def set_current_weather(self, weather_identifier: WeatherIdentifier) -> None:
        if not self.get_current_place_type() == PlaceType.AREA:
            raise ValueError(
                "Attempting to change the weather when the current place isn't an area!"
            )

        map_file = self._load_map_file()

        map_file[self._playthrough_manager.get_current_place_identifier()][
            "weather_identifier"
        ] = weather_identifier.value

        self._save_map_file(map_file)
