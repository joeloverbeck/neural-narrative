from dataclasses import dataclass
from typing import Any


@dataclass
class GetAreaInfoAlgorithmData:
    locations_present: list[dict[str, Any]]
    can_search_for_location: bool
    available_location_types: list[str]
    cardinal_connections: dict[str, dict[str, str] | None]
