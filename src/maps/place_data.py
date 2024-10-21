from dataclasses import dataclass
from typing import List, Optional

from src.base.required_string import RequiredString


@dataclass
class PlaceData:
    name: RequiredString
    description: RequiredString
    categories: List[RequiredString]
    type: Optional[RequiredString]  # Only for LOCATION templates
