import logging
from typing import List, Dict, Any, Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.map_repository import MapRepository

logger = logging.getLogger(__name__)


class GetPlacesInPlaceAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        containing_place_identifier: str,
        containing_place_type: TemplateType,
        contained_place_type: TemplateType,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(
            containing_place_identifier, "containing_place_identifier"
        )

        self._containing_place_identifier = containing_place_identifier
        self._containing_place_type = containing_place_type
        self._contained_place_type = contained_place_type

        self._map_repository = map_repository or MapRepository(playthrough_name)

    def do_algorithm(self) -> List[Dict[str, Any]]:
        map_file = self._map_repository.load_map_data()

        contained_places = []

        for identifier, data in map_file.items():
            if not data:
                raise ValueError(f"Found no data for place identifier '{identifier}'.")

            if (
                data.get(self._containing_place_type.value)
                == self._containing_place_identifier
                and data.get("type") == self._contained_place_type.value
            ):
                location_info = {
                    "identifier": identifier,
                    "place_template": data.get("place_template"),
                }

                contained_places.append(location_info)

        if not contained_places:
            logger.warning(
                f"No contained place type '{self._contained_place_type.value}' found in {self._containing_place_type.value} '{self._containing_place_identifier}'."
            )

        return contained_places
