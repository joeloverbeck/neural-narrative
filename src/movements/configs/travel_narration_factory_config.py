from dataclasses import dataclass


@dataclass
class TravelNarrationFactoryConfig:
    playthrough_name: str
    destination_identifier: str
    travel_context: str
