from dataclasses import dataclass
from typing import Any


@dataclass
class GetLocationInfoAlgorithmData:
    rooms_present: list[dict[str, Any]]
    can_search_for_room: bool
    available_room_types: list[str]
