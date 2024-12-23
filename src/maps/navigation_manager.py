import logging
from typing import Dict, Optional

from src.base.enums import TemplateType
from src.maps.enums import CardinalDirection
from src.maps.map_repository import MapRepository

logger = logging.getLogger(__name__)


class NavigationManager:

    def __init__(self, map_repository: MapRepository):
        self._map_repository = map_repository

    def does_area_have_cardinal_connection(
            self, area_identifier: str, cardinal_direction: CardinalDirection
    ) -> bool:
        map_data = self._map_repository.load_map_data()
        area_entry = map_data.get(area_identifier)
        if not area_entry or area_entry.get("type") != TemplateType.AREA.value:
            raise ValueError(f"'{area_identifier}' is not a valid area.")
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
        map_file = self._map_repository.load_map_data()
        if area_identifier not in map_file:
            raise ValueError(f"Area identifier '{area_identifier}' not found in map.")
        area_entry = map_file[area_identifier]
        if area_entry.get("type") != TemplateType.AREA.value:
            raise ValueError(
                f"The given identifier '{area_identifier}' is not an area, but a '{area_entry.get('type')}'."
            )
        result = {}
        for direction in [d for d in CardinalDirection]:
            connected_area_id = area_entry.get(direction.value)
            if connected_area_id:
                connected_area = map_file.get(connected_area_id)
                if not connected_area:
                    logger.warning(
                        f"Connected area '{connected_area_id}' not found in map."
                    )
                    result[direction.value] = None
                else:
                    place_template = connected_area.get("place_template")
                    if not place_template:
                        raise ValueError(
                            f"Place template not found for connected area '{connected_area_id}'."
                        )
                    result[direction.value] = {
                        "identifier": connected_area_id,
                        "place_template": place_template,
                    }
            else:
                result[direction.value] = None
        return result

    def create_cardinal_connection(
            self,
            cardinal_direction: CardinalDirection,
            origin_identifier: str,
            destination_identifier: str,
    ):
        map_data = self._map_repository.load_map_data()
        if cardinal_direction.value in map_data[origin_identifier]:
            raise ValueError(
                f"There was already a cardinal connection for '{cardinal_direction.value}' in '{origin_identifier}'."
            )
        map_data[origin_identifier][cardinal_direction.value] = destination_identifier
        self._map_repository.save_map_data(map_data)

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
