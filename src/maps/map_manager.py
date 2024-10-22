import logging
from typing import List, Dict, Optional

from src.base.enums import TemplateType
from src.base.identifiers_manager import IdentifiersManager
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.hierarchy_manager import HierarchyManager
from src.maps.map_repository import MapRepository
from src.maps.place_manager import PlaceManager
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class MapManager:

    def __init__(
        self,
            playthrough_name: str,
            place_manager: PlaceManager,
            map_repository: MapRepository,
            template_repository: TemplatesRepository,
            hierarchy_manager: Optional[HierarchyManager] = None,
        identifiers_manager: Optional[IdentifiersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._place_manager = place_manager
        self._map_repository = map_repository
        self._template_repository = template_repository
        self._hierarchy_manager = hierarchy_manager or HierarchyManager(
            self._place_manager
        )
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def get_story_universe_description(self) -> str:
        current_story_universe = self._playthrough_manager.get_story_universe_template()
        story_universe_templates_file = self._template_repository.load_template(
            TemplateType.STORY_UNIVERSE
        )
        if not current_story_universe in story_universe_templates_file:
            raise ValueError(
                f"Couldn't find the story universe '{current_story_universe}' in the file of templates."
            )
        story_universe_data = story_universe_templates_file[current_story_universe]
        if not "description" in story_universe_data:
            raise ValueError(
                f"Couldn't find a description for story universe '{current_story_universe}' in its data: {story_universe_data}"
            )
        return story_universe_data["description"]

    def get_current_place_template(self) -> str:
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        return self._place_manager.get_place_template(
            self._place_manager.get_place(current_place_id)
        )

    def get_current_area(self) -> dict:
        map_file = self._map_repository.load_map_data()
        if self._place_manager.get_current_place_type() == TemplateType.AREA:
            return map_file[self._playthrough_manager.get_current_place_identifier()]
        if not self._place_manager.get_current_place_type() == TemplateType.LOCATION:
            raise ValueError(
                f"At this point, wasn't expecting the current location to be {self._place_manager.get_current_place_type()}"
            )
        current_area_identifier = map_file[
            self._playthrough_manager.get_current_place_identifier()
        ]["area"]
        return map_file[current_area_identifier]

    def get_father_template(self) -> str:
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        places_parameter = self._hierarchy_manager.fill_places_templates_parameter(
            current_place_id
        )
        current_place_type = self._place_manager.get_current_place_type()
        if current_place_type == TemplateType.LOCATION:
            return places_parameter.get_area_template()
        if current_place_type == TemplateType.AREA:
            return places_parameter.get_region_template()
        if current_place_type == TemplateType.REGION:
            return places_parameter.get_world_template()
        raise ValueError(
            f"This function isn't prepared to handle the place type '{current_place_type}'."
        )

    def get_identifier_and_place_template_of_latest_map_entry(self) -> (str, str):
        map_file = self._map_repository.load_map_data()
        max_id_str = self._identifiers_manager.get_highest_identifier(map_file)
        place = self._place_manager.get_place(max_id_str)
        place_template = self._place_manager.get_place_template(place)
        return max_id_str, place_template

    def get_place_full_data(
            self, place_identifier: str
    ) -> Dict[str, Optional[Dict[str, str]]]:
        hierarchy = self._hierarchy_manager.get_place_hierarchy(place_identifier)
        result = {
            "world_data": None,
            "region_data": None,
            "area_data": None,
            "location_data": None,
        }
        for place_type in ["world", "region", "area", "location"]:
            place = hierarchy.get(place_type)
            if place:
                template_name = self._place_manager.get_place_template(place)
                templates = self._template_repository.load_template(
                    TemplateType(place_type)
                )
                template_data = templates.get(template_name)
                if not template_data:
                    raise ValueError(
                        f"{place_type.capitalize()} template '{template_name}' not found."
                    )
                result_data: Dict[str, str] = {
                    "name": template_name,
                    "description": template_data.get("description"),
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
        map_file = self._map_repository.load_map_data()
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
