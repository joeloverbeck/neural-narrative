from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PlaceData:
    name: str
    description: str
    categories: List[str]
    type: Optional[str]
