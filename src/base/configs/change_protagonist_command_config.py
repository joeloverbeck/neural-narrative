from dataclasses import dataclass


@dataclass
class ChangeProtagonistCommandConfig:
    playthrough_name: str
    new_protagonist_identifier: str
