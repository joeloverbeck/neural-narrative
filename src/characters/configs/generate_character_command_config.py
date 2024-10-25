from dataclasses import dataclass


@dataclass
class GenerateCharacterCommandConfig:
    playthrough_name: str
    place_character_at_current_place: bool
