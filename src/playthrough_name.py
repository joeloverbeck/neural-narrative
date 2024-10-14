from dataclasses import dataclass


@dataclass
class PlaythroughName:
    value: str

    def __post_init__(self):
        if not self.is_valid():
            raise ValueError(f"Invalid playthrough name: {self.value}")

    def is_valid(self) -> bool:
        if not self.value:
            return False

        return True
