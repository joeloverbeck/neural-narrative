from dataclasses import dataclass
from pathlib import Path


@dataclass
class VoicePartProviderConfig:
    part: str
    xtts_endpoint: str
    timestamp: str
    index: int
    temp_dir: Path

    def __post_init__(self):
        if not self.part:
            raise ValueError("part can't be empty.")
        if not self.xtts_endpoint:
            raise ValueError("xtts_endpoint can't be empty.")
        if not self.timestamp:
            raise ValueError("timestamp can't be empty.")
        if self.index < 0:
            raise ValueError(f"Invalid index: {self.index}.")
