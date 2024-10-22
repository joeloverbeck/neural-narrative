from dataclasses import dataclass
from src.maps.enums import CardinalDirection


@dataclass
class CardinalConnectionCreationFactoryConfig:
    playthrough_name: str
    cardinal_direction: CardinalDirection
