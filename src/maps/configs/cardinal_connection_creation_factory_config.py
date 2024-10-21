from dataclasses import dataclass

from src.base.required_string import RequiredString
from src.maps.enums import CardinalDirection


@dataclass
class CardinalConnectionCreationFactoryConfig:
    playthrough_name: RequiredString
    cardinal_direction: CardinalDirection
