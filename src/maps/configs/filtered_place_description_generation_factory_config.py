from dataclasses import dataclass


@dataclass
class FilteredPlaceDescriptionGenerationFactoryConfig:
    playthrough_name: str
    place_identifier: str
