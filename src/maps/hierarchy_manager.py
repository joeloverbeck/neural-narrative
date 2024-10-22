from typing import Optional, Dict

from src.base.enums import TemplateType
from src.maps.place_manager import PlaceManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class HierarchyManager:

    def __init__(self, place_manager: PlaceManager):
        self._place_manager = place_manager

    def get_place_hierarchy(self, place_identifier: str) -> Dict[str, Optional[Dict]]:
        hierarchy = {"world": None, "region": None, "area": None, "location": None}
        current_place_id = place_identifier
        while current_place_id:
            place = self._place_manager.get_place(current_place_id)
            place_type = self._place_manager.determine_place_type(current_place_id)
            if place_type == TemplateType.WORLD:
                hierarchy["world"] = place
                break
            elif place_type == TemplateType.REGION:
                hierarchy["region"] = place
                current_place_id = place.get("world")
            elif place_type == TemplateType.AREA:
                hierarchy["area"] = place
                if not "region" in place:
                    raise ValueError("Area didn't have 'region' assigned.")
                region_identifier = place.get("region")
                if not region_identifier:
                    raise ValueError("Area didn't have a proper 'region' assigned.")
                current_place_id = region_identifier
            elif place_type == TemplateType.LOCATION:
                hierarchy["location"] = place
                current_place_id = place.get("area")
            else:
                raise ValueError(f"Unhandled place type '{place_type.value}'.")
        if not hierarchy["world"]:
            raise ValueError("World not found in the place hierarchy.")
        return hierarchy

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
        place = self._place_manager.get_place(place_identifier)
        place_type = self._place_manager.determine_place_type(place_identifier)
        if place_type == TemplateType.AREA:
            father_identifier = place.get("region")
            if not father_identifier:
                raise ValueError(f"Area '{place_identifier}' has no 'region' key.")
            return father_identifier
        elif place_type == TemplateType.LOCATION:
            father_identifier = place.get("area")
            if not father_identifier:
                raise ValueError(f"Location '{place_identifier}' has no 'area' key.")
            return father_identifier
        elif place_type == TemplateType.REGION:
            father_identifier = place.get("world")
            if not father_identifier:
                raise ValueError(f"Region '{place_identifier}' has no 'world' key.")
            return father_identifier
        elif place_type == TemplateType.WORLD:
            raise ValueError(f"Region '{place_identifier}' has no father identifier.")
        else:
            raise ValueError(
                f"Unhandled place type '{place_type}' for identifier '{place_identifier}'."
            )

    def fill_places_templates_parameter(
        self, place_identifier: str
    ) -> PlacesTemplatesParameter:
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")
        hierarchy = self.get_place_hierarchy(place_identifier)
        world_template = self._place_manager.get_place_template(hierarchy["world"])
        region_template = (
            self._place_manager.get_place_template(hierarchy["region"])
            if hierarchy["region"]
            else world_template
        )
        area_template = (
            self._place_manager.get_place_template(hierarchy["area"])
            if hierarchy["area"]
            else region_template
        )
        location_template = (
            self._place_manager.get_place_template(hierarchy["location"])
            if hierarchy["location"]
            else None
        )
        return PlacesTemplatesParameter(
            world_template=world_template,
            region_template=region_template,
            area_template=area_template,
            location_template=location_template,
        )
