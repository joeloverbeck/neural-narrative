import traceback
from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass
class RequiredString:
    value: str

    def __init__(self, value):
        if not value:
            raise ValueError("value can't be empty.")

        if isinstance(value, RequiredString):
            self.value = value.value
        elif not isinstance(value, str):
            raise TypeError("value must be a string")
        else:
            self.value = value

    def __post_init__(self):
        if not self._is_valid():
            traceback.print_exc()
            raise ValueError(f"Invalid value: {self.value}")

    def _is_valid(self) -> bool:
        if not self.value:
            return False

        return True

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, RequiredString):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, RequiredString):
            return self.value < other.value
        return NotImplemented

    def __repr__(self):
        return f"RequiredString(value='{self.value}')"
