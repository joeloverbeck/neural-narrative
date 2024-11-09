from typing import Optional, Dict

from src.base.constants import PARENT_KEYS
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.place_manager import PlaceManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class HierarchyManager:

    def __init__(self, place_manager: PlaceManager):
        self._place_manager = place_manager

    def get_place_hierarchy(self, place_identifier: str) -> Dict[str, Optional[Dict]]:
        hierarchy = {
            "world": None,
            "region": None,
            "area": None,
            "location": None,
            "room": None,
        }

        current_place_id = place_identifier

        while current_place_id:
            place = self._place_manager.get_place(current_place_id)
            place_type = self._place_manager.determine_place_type(current_place_id)

            if place_type == TemplateType.WORLD:
                hierarchy[place_type.value] = place
                break

            if (
                place_type == TemplateType.REGION
                or place_type == TemplateType.AREA
                or place_type == TemplateType.LOCATION
                or place_type == TemplateType.ROOM
            ):
                if not place:
                    raise ValueError(
                        f"Didn't have a 'place' for place type '{place_type}'."
                    )

                hierarchy[place_type.value] = place

                parent_key = PARENT_KEYS.get(place_type)

                if not parent_key in place.keys():
                    raise KeyError(
                        f"The parent key '{parent_key}' wasn't present in the place data: {place}"
                    )

                current_place_id = place.get(parent_key)
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

        if (
            place_type == TemplateType.ROOM
            or place_type == TemplateType.LOCATION
            or place_type == TemplateType.AREA
            or place_type == TemplateType.REGION
        ):
            parent_key = PARENT_KEYS.get(place_type)
            father_identifier = place.get(parent_key)
            if not father_identifier:
                raise ValueError(
                    f"Location '{place_identifier}' has no '{parent_key}' key."
                )
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
        validate_non_empty_string(place_identifier, "place_identifier")

        hierarchy = self.get_place_hierarchy(place_identifier)
        world_template = self._place_manager.get_place_template(
            hierarchy[TemplateType.WORLD.value]
        )

        region_template = (
            self._place_manager.get_place_template(hierarchy[TemplateType.REGION.value])
            if hierarchy[TemplateType.REGION.value]
            else world_template
        )
        area_template = (
            self._place_manager.get_place_template(hierarchy[TemplateType.AREA.value])
            if hierarchy[TemplateType.AREA.value]
            else region_template
        )
        location_template = (
            self._place_manager.get_place_template(
                hierarchy[TemplateType.LOCATION.value]
            )
            if hierarchy[TemplateType.LOCATION.value]
            else None
        )

        return PlacesTemplatesParameter(
            world_template=world_template,
            region_template=region_template,
            area_template=area_template,
            location_template=location_template,
        )
