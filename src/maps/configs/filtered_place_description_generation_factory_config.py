from dataclasses import dataclass

from src.base.required_string import RequiredString


@dataclass
class FilteredPlaceDescriptionGenerationFactoryConfig:
    playthrough_name: RequiredString
    place_identifier: RequiredString
