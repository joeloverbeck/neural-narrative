from dataclasses import dataclass


@dataclass
class GenerateCharacterImageCommandConfig:
    playthrough_name: str
    character_identifier: str
