from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class GetPlaceInfoAlgorithmData:
    locations_present: Optional[list[dict[str, Any]]]
    can_search_for_location: bool
    available_location_types: list[str]
    cardinal_connections: Optional[dict[str, dict[str, str] | None]]
    rooms_present: Optional[list[dict[str, Any]]]
    can_search_for_room: bool
    available_room_types: list[str]
