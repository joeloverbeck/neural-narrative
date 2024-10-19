from dataclasses import dataclass


@dataclass
class RequiredString:
    value: str

    def __post_init__(self):
        if not self.is_valid():
            raise ValueError(f"Invalid value: {self.value}")

    def is_valid(self) -> bool:
        if not self.value:
            return False

        return True

    def __str__(self):
        return self.value
