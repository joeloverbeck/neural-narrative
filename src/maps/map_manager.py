import logging.config
import random
from typing import List

from src.enums import PlaceType
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter

logger = logging.getLogger(__name__)


class MapManager:
    def __init__(self, playthrough_name: str, filesystem_manager: FilesystemManager = None,
                 identifiers_manager: IdentifiersManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")

        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(playthrough_name)

    def get_current_place_identifier(self, playthrough_name: str):
        assert playthrough_name

        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(playthrough_name))

        return playthrough_metadata["current_place"]

    def get_place_categories(self, place_template: str, place_type: PlaceType) -> List[str]:
        if place_type == PlaceType.WORLD:
            templates_file_path = self._filesystem_manager.get_file_path_to_worlds_template_file()
        elif place_type == PlaceType.REGION:
            templates_file_path = self._filesystem_manager.get_file_path_to_regions_template_file()
        elif place_type == PlaceType.AREA:
            templates_file_path = self._filesystem_manager.get_file_path_to_areas_template_file()
        else:
            raise ValueError(f"I didn't program getting the place categories of '{place_type.value}'.")

        """Retrieve categories for the specified place type."""
        place_data = self._filesystem_manager.load_existing_or_new_json_file(
            templates_file_path).get(place_template)

        if not place_data:
            raise ValueError(f"'{place_template}' not found in {place_type.value}.")
        return place_data.get('categories', [])

    @staticmethod
    def filter_places_by_categories(place_templates: dict, father_place_categories: List[str]):
        """Filter places whose categories match any of the father place's categories."""
        matching_regions = {}

        for region_name, region_data in place_templates.items():
            region_categories = region_data.get('categories', [])
            if set(region_categories) & set(father_place_categories):
                matching_regions[region_name] = region_data

        return matching_regions

    @staticmethod
    def select_random_place(matching_places: dict):
        """Select a random place from the matching places."""
        if not matching_places:
            raise ValueError(
                "The matching places were empty. Maybe you need to generate places of that type from the wanted father place.")

        return random.choice(list(matching_places.keys()))

    def get_identifier_and_place_template_of_latest_map_entry(self) -> (str, str):
        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        max_id_str = self._identifiers_manager.get_highest_identifier(map_file)

        # Retrieve the "place_template" for the maximum identifier
        place_template = map_file[max_id_str]["place_template"]

        return max_id_str, place_template

    def fill_places_parameter(self, place_identifier: str):
        if not place_identifier:
            raise ValueError("place_identifier should not be empty.")

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        # Retrieve the place data
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID {place_identifier} not found")

        # Initialize templates
        region_template = None
        area_template = None
        location_template = None

        # Determine the type of the place
        place_type = place.get('type')

        if place_type == PlaceType.LOCATION.value:
            # Get location_template
            location_template = place.get('place_template')

            # Get area data
            area_id = place.get('area')
            if not area_id:
                raise ValueError(f"Area ID not found for location {place_identifier}")
            area = map_file.get(area_id)
            if not area:
                raise ValueError(f"Area {area_id} not found")

            # Get area_template
            area_template = area.get('place_template')

            # Get region data
            region_id = area.get('region')
            if not region_id:
                raise ValueError(f"Region ID not found for area {area_id}")
            region = map_file.get(region_id)
            if not region:
                raise ValueError(f"Region {region_id} not found")

            # Get region_template
            region_template = region.get('place_template')

        elif place_type == PlaceType.AREA.value:
            # Get area_template
            area_template = place.get('place_template')

            # Get region data
            region_id = place.get('region')
            if not region_id:
                raise ValueError(f"Region ID not found for area {place_identifier}")
            region = map_file.get(region_id)
            if not region:
                raise ValueError(f"Region {region_id} not found")

            # Get region_template
            region_template = region.get('place_template')

        elif place_type == PlaceType.REGION.value:
            # Get region_template
            region_template = place.get('place_template')

            # Since area_template is required, we'll set it to the same as region_template
            area_template = region_template
        else:
            raise ValueError(f"Unknown place type {place_type} for place ID {place_identifier}")

        places_parameter = PlacesTemplatesParameter(
            region_template=region_template,
            area_template=area_template,
            location_template=location_template
        )

        return places_parameter

    def place_character_at_place(self, character_identifier, place_identifier):
        if not character_identifier:
            raise ValueError("character_identifier should not be empty.")
        if not place_identifier:
            raise ValueError("place_identifier should not be empty.")

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        # Get the place data
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID {place_identifier} not found.")

        # Ensure the place type is 'area' or 'location'
        place_type = place.get('type')
        if place_type not in ('area', 'location'):
            raise ValueError(f"Place type '{place_type}' cannot house characters.")

        # Get the 'characters' list
        characters_list = place.get('characters')
        if characters_list is None:
            # Initialize the list if not present
            characters_list = []
            place['characters'] = characters_list

        # Check if character is already present
        if character_identifier in characters_list:
            raise ValueError(f"Character {character_identifier} is already at place {place_identifier}.")

        # Add the character identifier to the list
        characters_list.append(character_identifier)

        # Save the updated map file
        self._filesystem_manager.save_json_file(map_file,
                                                self._filesystem_manager.get_file_path_to_map(self._playthrough_name))

        logger.info(
            f"Character '{character_identifier}' placed at {place_type} '{place_identifier}'. Current character list: {characters_list}")

    def get_place_full_data(self, place_identifier: str) -> dict:
        if not place_identifier:
            raise ValueError("place_identifier should not be empty.")

        map_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_map(self._playthrough_name)
        )

        # Retrieve the place data
        place = map_file.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID {place_identifier} not found.")

        # Initialize the result dictionary
        result = {
            "region_data": None,
            "area_data": None,
            "location_data": None
        }

        # Determine the type of the place
        place_type = place.get('type')

        if place_type == PlaceType.LOCATION.value:
            # Get location data
            location_template = place.get('place_template')
            location_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_locations_template_file()
            )
            location_data = location_templates.get(location_template)
            if not location_data:
                raise ValueError(f"Location template '{location_template}' not found.")

            result['location_data'] = {
                'name': location_template,
                'description': location_data.get('description', '')
            }

            # Get area data
            area_id = place.get('area')
            if not area_id:
                raise ValueError(f"Area ID not found for location {place_identifier}.")
            area = map_file.get(area_id)
            if not area:
                raise ValueError(f"Area {area_id} not found.")

            area_template = area.get('place_template')
            area_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_areas_template_file()
            )
            area_data = area_templates.get(area_template)
            if not area_data:
                raise ValueError(f"Area template '{area_template}' not found.")

            result['area_data'] = {
                'name': area_template,
                'description': area_data.get('description', '')
            }

            # Get region data
            region_id = area.get('region')
            if not region_id:
                raise ValueError(f"Region ID not found for area {area_id}.")
            region = map_file.get(region_id)
            if not region:
                raise ValueError(f"Region {region_id} not found.")

            region_template = region.get('place_template')
            region_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_regions_template_file()
            )
            region_data = region_templates.get(region_template)
            if not region_data:
                raise ValueError(f"Region template '{region_template}' not found.")

            result['region_data'] = {
                'name': region_template,
                'description': region_data.get('description', '')
            }

        elif place_type == PlaceType.AREA.value:
            # Get area data
            area_template = place.get('place_template')
            area_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_areas_template_file()
            )
            area_data = area_templates.get(area_template)
            if not area_data:
                raise ValueError(f"Area template '{area_template}' not found.")

            result['area_data'] = {
                'name': area_template,
                'description': area_data.get('description', '')
            }

            # Get region data
            region_id = place.get('region')
            if not region_id:
                raise ValueError(f"Region ID not found for area {place_identifier}.")
            region = map_file.get(region_id)
            if not region:
                raise ValueError(f"Region {region_id} not found.")

            region_template = region.get('place_template')
            region_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_regions_template_file()
            )
            region_data = region_templates.get(region_template)
            if not region_data:
                raise ValueError(f"Region template '{region_template}' not found.")

            result['region_data'] = {
                'name': region_template,
                'description': region_data.get('description', '')
            }

        elif place_type == PlaceType.REGION.value:
            # Get region data
            region_template = place.get('place_template')
            region_templates = self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_regions_template_file()
            )
            region_data = region_templates.get(region_template)
            if not region_data:
                raise ValueError(f"Region template '{region_template}' not found.")

            result['region_data'] = {
                'name': region_template,
                'description': region_data.get('description', '')
            }

        else:
            raise ValueError(f"Unknown place type '{place_type}' for place ID {place_identifier}.")

        return result
