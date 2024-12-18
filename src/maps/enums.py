from enum import Enum


class RandomTemplateTypeMapEntryCreationResultType(Enum):
    FAILURE = 'failure'
    SUCCESS = 'success'
    NO_AVAILABLE_TEMPLATES = 'no_available_templates'


class CardinalDirection(Enum):
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
